from typing import Protocol


class IHandler(Protocol):
    def callback(self, message: dict) -> None:
        pass
