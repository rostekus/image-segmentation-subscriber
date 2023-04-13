import logging
import queue
from typing import Type

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class SingletonMeta(type):
    _instances: dict[Type["SingletonMeta"], "SingletonMeta"] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class QueueBroker(metaclass=SingletonMeta):
    def __init__(self):
        self._queue = queue.Queue()

    def register(self, message: dict) -> None:
        self._queue.put(message)

    @staticmethod
    def processing_queue():
        pass
