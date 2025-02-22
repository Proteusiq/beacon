from pathlib import Path
from typing import Final

import polars as pl

# TODO: goes to config.py
DATA_URI: Path = Path("data/goodreads_top100_from1980to2023_final.csv")
LANGUAGE: Final = "English"
NUMBER_REVIEWS: Final = 300


def get_data() -> pl.DataFrame:
    schema_overrides = {"isbn": pl.Utf8}

    books = (
        pl.read_csv(
            DATA_URI,
            schema_overrides=schema_overrides,
        )
        .filter(pl.col("language").eq(LANGUAGE) & pl.col("num_reviews").ge(NUMBER_REVIEWS))
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
