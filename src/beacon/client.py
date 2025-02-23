import types

from qdrant_client import QdrantClient


class Client:
    def __init__(self, path: str):
        self.path = path

    def __enter__(self) -> QdrantClient:
        self.client = QdrantClient(path=self.path)
        return self.client

    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: types.TracebackType | None
    ) -> None:
        self.client.close()
