from beacon.pan.db_client import BookDatabase
from beacon.pan.oil import get_data
from beacon.settings import DEFAULT_LIMIT


def load_data() -> None:
    """load and store books data in the vector database.

    reads book data from csv, processes it, and stores in the vector database
    with metadata for efficient similarity search. this needs to be run once
    before making recommendations.
    """
    db = BookDatabase()
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
    db.add_books(documents=documents, metadata=metadata)


def get_recommendation(text: str, limit: int = DEFAULT_LIMIT) -> list[dict[str, str]]:
    """find books similar to the provided text description.

    args:
        text: query text describing desired book content/theme
        limit: maximum number of recommendations to return (default: from settings)

    returns:
        list of dictionaries containing book recommendations with:
            - title: book title (with series info if applicable)
            - author: book author name
    """
    db = BookDatabase()
    results = db.query_books(text=text, limit=limit)
    return [{"title": r.metadata["title"], "author": r.metadata["author"]} for r in results]
