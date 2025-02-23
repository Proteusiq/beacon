from beacon.client import Client
from beacon.settings import BOOKS_DB_PATH, DEFAULT_COLLECTION_NAME, DEFAULT_LIMIT


def get(text, limit=DEFAULT_LIMIT, collection_name=DEFAULT_COLLECTION_NAME):
    with Client(path=str(BOOKS_DB_PATH)) as client:
        return client.query(
            collection_name=collection_name,
            query_text=text,
            limit=limit,
        )


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

    results = get(text=text, limit=limit)
    return [{"title": r.metadata["title"], "author": r.metadata["author"]} for r in results]
