from beacon.client import Client
from beacon.settings import BOOKS_DB_PATH, DEFAULT_COLLECTION_NAME


def post(documents: list[str], metadata: list[dict[str, str]], collection_name: str = DEFAULT_COLLECTION_NAME) -> None:
    with Client(path=str(BOOKS_DB_PATH)) as client:
        client.add(
            collection_name=collection_name,
            documents=documents,
            metadata=metadata,
        )
