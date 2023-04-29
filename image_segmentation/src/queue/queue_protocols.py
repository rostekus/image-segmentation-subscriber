from abc import abstractmethod
from typing import Protocol


class IHandler(Protocol):
    def register(self, message: bytes) -> None:
        pass

    def set_next(self, handler: "IHandler") -> "IHandler":
        pass


class AbstractHandler:
    _next_handler: IHandler | None = None

    def set_next(self, handler: IHandler) -> IHandler:
        self._next_handler = handler
        return handler

    @abstractmethod
    def register(self, message: bytes) -> None:
        if self._next_handler:
            return self._next_handler.register(message)
        return None


class IPublisher(Protocol):
    def __init__(self, queue: str):
        pass

    def publish(self, message: bytes):
        pass


class ISubscriber(Protocol):
    def __init__(self, queue: str, request_handler: IHandler):
        pass

    def start_consuming(self):
        pass
