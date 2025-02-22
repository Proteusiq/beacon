from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.http.models import QueryResponse

from beacon.settings import BOOKS_DB_PATH


class BookDatabase:
    def __init__(self) -> None:
        self.client = QdrantClient(path=str(BOOKS_DB_PATH))

    def add_books(self, documents: list[str], metadata: list[dict[str, Any]]) -> None:
        """Add books to the database with their metadata."""
        self.client.add(
            collection_name="books",
            documents=documents,
            metadata=metadata,
        )

    def query_books(self, text: str, limit: int) -> list[QueryResponse]:
        """Query books based on text similarity."""
        return self.client.query(
            collection_name="books",
            query_text=text,
            limit=limit,
        )
