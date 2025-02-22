from beacon.pan.db_client import BookDatabase
from beacon.pan.oil import get_data
from beacon.settings import DEFAULT_LIMIT


def load_data() -> None:
    """Load books data into the database."""
    db = BookDatabase()
    books_df = get_data()
    
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
    """Get book recommendations based on text similarity."""
    db = BookDatabase()
    results = db.query_books(text=text, limit=limit)
    return [{"title": r.metadata["title"], "author": r.metadata["author"]} for r in results]
