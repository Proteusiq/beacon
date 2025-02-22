import polars as pl

from beacon.settings import BOOKS_CSV_PATH, LANGUAGE, MIN_REVIEWS


def get_data() -> pl.DataFrame:
    """Load and preprocess books data from CSV."""
    schema_overrides = {"isbn": pl.Utf8}

    books = (
        pl.read_csv(
            BOOKS_CSV_PATH,
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
