from typing import Protocol

from src.queue.handler.handler_protocol import IHandler


class ISubscriber(Protocol):
    def __init__(self, queue: str, request_handler: IHandler):
        pass

    def start_consuming(self):
        pass
