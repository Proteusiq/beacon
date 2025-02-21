import marimo

__generated_with = "0.11.7"
app = marimo.App(width="medium")


@app.cell
def _(Final, llama_cpp):
    MODEL_PATH: Final = "model/gemma-1.1-2b-it-Q4_K_M.gguf"

    llm = llama_cpp.Llama(model_path=MODEL_PATH, embedding=True, pooling_type=llama_cpp.LLAMA_POOLING_TYPE_CLS)
    return MODEL_PATH, llm


@app.cell
def _(llm):
    embeddings = llm.create_embedding(["Hello, world!", "Hej Planet Earth"])
    return (embeddings,)


@app.cell
def _(embeddings):
    embeddings
    return


@app.cell
def _(List, np, spatial):
    # Stolen from OpenAI cookbook

    def cosine_similarity(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def indices_of_nearest_neighbors_from_distances(distances) -> np.ndarray:
        """Return a list of indices of nearest neighbors from a list of distances."""
        return np.argsort(distances)

    def distances_from_embeddings(
        query_embedding: List[float],
        embeddings: List[List[float]],
        distance_metric="cosine",
    ) -> List[List]:
        """Return the distances between a query embedding and a list of embeddings."""
        distance_metrics = {
            "cosine": spatial.distance.cosine,
            "L1": spatial.distance.cityblock,
            "L2": spatial.distance.euclidean,
            "Linf": spatial.distance.chebyshev,
        }
        distances = [
            distance_metrics[distance_metric](query_embedding, embedding)
            for embedding in embeddings
        ]
        return distances
    return (
        cosine_similarity,
        distances_from_embeddings,
        indices_of_nearest_neighbors_from_distances,
    )


@app.cell
def _(becons, pl):
    becons.filter(pl.col("combined_title").str.contains("Harry Potter"))
    return


@app.cell
def _(Final, books, pl):
    LANGUAGE: Final = "English"
    NUMBER_REVIEWS: Final = 300

    becons = (books
      .filter(pl.col("language").eq(LANGUAGE) & pl.col("num_reviews").ge(NUMBER_REVIEWS))
      .select(
          [pl.col("isbn"), 
           pl.col("title"),
           pl.col("series_title"),
           pl.col("authors"),
           pl.col("rating_score"),
           pl.col("num_ratings"),
           pl.col("num_reviews"),
           pl.col("want_to_read"),
           pl.col("genres"),
           pl.col("description")
          ]
      )
      .with_columns([
          pl.when(
            (pl.col('series_title').is_not_null())& 
            (~pl.col('title').str.contains(pl.col('series_title')))
        )
        .then(pl.col('series_title') + ': ' + pl.col('title')) # pl.concat_str([pl.col('series_title'), pl.lit(': '), pl.col('title')])
        .otherwise(pl.col('title'))
        .alias('combined_title')
        ])
     .drop([pl.col("title"), 
            pl.col("series_title")
           ])

    )

    becons
    return LANGUAGE, NUMBER_REVIEWS, becons


@app.cell
def _(pl):
    DATA_URI:str = "data/goodreads_top100_from1980to2023_final.csv"

    schema_overrides = {"isbn": pl.Utf8}

    books = (pl
     .read_csv(DATA_URI, 
               schema_overrides=schema_overrides,
             )
    )
    books
    return DATA_URI, books, schema_overrides


@app.cell
def _():
    import marimo as mo
    import polars as pl
    import altair as alt
    import numpy as np
    from scipy import spatial
    return alt, mo, np, pl, spatial


@app.cell
def _():
    import llama_cpp
    return (llama_cpp,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
