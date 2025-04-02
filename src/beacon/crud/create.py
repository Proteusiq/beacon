import polars as pl

from beacon.crud import upload
from beacon.settings import BOOKS_CSV_URI, LANGUAGE, MIN_REVIEWS


def get_data(test_mode: bool = False) -> pl.DataFrame:
    """load and preprocess books data from csv file.

    reads the books dataset and applies filtering and transformations:
    - filters for english books with minimum review threshold
    - combines series title with book title when applicable
    - selects relevant columns for recommendation system

    args:
        test_mode: if True, only loads a small subset of data for testing

    returns:
        polars dataframe with processed book data containing:
        - isbn, combined_title, authors, ratings, reviews
        - genres, description and other metadata
    """
    schema_overrides = {"isbn": pl.Utf8}

    books = (
        pl.read_csv(
            BOOKS_CSV_URI,
            schema_overrides=schema_overrides,
        )
        .filter(pl.col("language").eq(LANGUAGE) & pl.col("num_reviews").ge(MIN_REVIEWS))
        .select([
            pl.col("isbn"),
            pl.col("title"),
            pl.col("series_title"),
            pl.col("authors"),
            pl.col("rating_score"),
            pl.col("num_ratings"),
            pl.col("num_reviews"),
            pl.col("want_to_read"),
            pl.col("genres"),
            pl.col("description"),
        ])
        .with_columns([
            pl.when((pl.col("series_title").is_not_null()) & (~pl.col("title").str.contains(pl.col("series_title"))))
            .then(
                pl.col("series_title") + ": " + pl.col("title")
            )  # pl.concat_str([pl.col('series_title'), pl.lit(': '), pl.col('title')])
            .otherwise(pl.col("title"))
            .alias("combined_title")
        ])
        .drop(["title", "series_title"])
    )

    # For test mode, only get the targeted books
    if test_mode:
        # Get books with specific keywords for tests
        return books.filter(pl.col("description").str.contains("(?i)lawyer|wizard|vampire"))
    
    # For regular mode, get a sample plus the targeted books
    targeted = books.filter(pl.col("description").str.contains("(?i)lawyer|wizard|vampire"))
    books = books.sample(50, seed=42).extend(targeted)

    return books


def create_db(test_mode: bool = False) -> None:
    """load and store books data in the vector database.

    with metadata for efficient similarity search. this needs to be run once
    before making recommendations. will only load data if the books directory
    is empty or doesn't exist.

    args:
        test_mode: if True, only loads test data (smaller dataset)
    """
    books_df = get_data(test_mode=test_mode)

    metadata = [
        {
            "author": author,
            "title": title,
        }
        for author, title in zip(
            books_df.select("authors").get_column("authors").to_list(),
            books_df.select("combined_title").get_column("combined_title").to_list(),
        )
    ]
    documents = books_df.select("description").get_column("description").to_list()
    upload.post(documents=documents, metadata=metadata)
