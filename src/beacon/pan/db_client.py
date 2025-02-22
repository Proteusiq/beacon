from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.http.models import QueryResponse

from beacon.settings import BOOKS_DB_PATH


class BookDatabase:
    """handles book storage and retrieval using vector similarity search.
    
    this class manages the interaction with the qdrant vector database for storing
    and querying book information. it provides methods to add books with their
    metadata and search for similar books based on text descriptions.
    """

    def __init__(self) -> None:
        """initialize database connection using configured path."""
        self.client = QdrantClient(path=str(BOOKS_DB_PATH))

    def add_books(self, documents: list[str], metadata: list[dict[str, Any]]) -> None:
        """add books and their metadata to the database.
        
        args:
            documents: list of book descriptions or content
            metadata: list of dictionaries containing book metadata (author, title)
        """
        self.client.add(
            collection_name="books",
            documents=documents,
            metadata=metadata,
        )

    def query_books(self, text: str, limit: int) -> list[QueryResponse]:
        """find similar books based on text description.
        
        args:
            text: query text to match against book descriptions
            limit: maximum number of results to return
            
        returns:
            list of QueryResponse objects containing matched books and their metadata
        """
        return self.client.query(
            collection_name="books",
            query_text=text,
            limit=limit,
        )
