from typing import Protocol


class DBConnection(Protocol):
    def __enter__(self):
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        ...

    def download_file(self, filename: str) -> bytes:
        ...

    def upload_file(self, filename: str, file: bytes) -> None:
        ...
