from qdrant_client import QdrantClient


class Client:
    def __init__(self, path: str):
        self.path = path

    def __enter__(self) -> QdrantClient:
        self.client = QdrantClient(path=self.path)
        return self.client

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.client.close()
