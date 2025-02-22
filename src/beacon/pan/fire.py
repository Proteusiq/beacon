from qdrant_client import QdrantClient
from qdrant_client.http.models import QueryResponse

from beacon.pan.oil import get_data

client = QdrantClient(path="data/books")


def load_data() -> None:
    bacons = get_data()
    metadata = [
        {
            "author": author,
            "title": title,
        }
        for author, title in zip(
            bacons.select("authors").get_column("authors").to_list(),
            bacons.select("combined_title").get_column("combined_title").to_list(),
        )
    ]
    documents = bacons.select("description").get_column("description").to_list()
    client.add(
        collection_name="books",
        documents=documents,
        metadata=metadata,
    )


def get_recommendation(text: str, limit: int = 5) -> list[type(QueryResponse)]:
    return client.query(
        collection_name="books",
        query_text=text,
        limit=limit,
    )
