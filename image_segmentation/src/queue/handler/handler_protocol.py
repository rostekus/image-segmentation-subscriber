from typing import Protocol


class IHandler(Protocol):
    def register(self, message: bytes) -> None:
        pass
