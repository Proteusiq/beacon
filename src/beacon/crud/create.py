import polars as pl

from beacon.crud import upload
from beacon.settings import BOOKS_CSV_URI, BOOKS_DB_PATH, LANGUAGE, MIN_REVIEWS


def get_data() -> pl.DataFrame:
    """load and preprocess books data from csv file.

    reads the books dataset and applies filtering and transformations:
    - filters for english books with minimum review threshold
    - combines series title with book title when applicable
    - selects relevant columns for recommendation system

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

    return books


def create_db() -> None:
    """load and store books data in the vector database.

    reads book data from csv, processes it, and stores in the vector database
    with metadata for efficient similarity search. this needs to be run once
    before making recommendations. will only load data if the books directory
    is empty or doesn't exist.
    """
    # create books directory if it doesn't exist
    BOOKS_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    BOOKS_DB_PATH.mkdir(exist_ok=True)

    # early return if directory is empty
    if any(BOOKS_DB_PATH.iterdir()):
        print("green")
        return

    # create db
    print("creation")
    books_df = get_data()

    # extract metadata and descriptions for storage
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
