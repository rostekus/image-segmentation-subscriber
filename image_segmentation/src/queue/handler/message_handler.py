import json
import logging
import queue
from typing import Type

from src.image_segmentation.image_segmentation_model.segmentatin_model_factory import (
    SegmentationModelFactory,
)



class SingletonMeta(type):
    _instances: dict[Type["SingletonMeta"], "SingletonMeta"] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class QueueBroker(metaclass=SingletonMeta):
    def __init__(self, image_segmentation_factory: SegmentationModelFactory):
        self._queue: queue.Queue = queue.Queue()
        self._image_segmentation_factory = image_segmentation_factory

    def register(self, message: bytes) -> None:
        try:
            logging.info("registering message: %s", message)
            message = json.loads(message)
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            logger.error(f"message is not a valid json. {message!r}. error: {e}")
            return
        self._queue.put(message)

    def processing_queue(self):
        while True:
            if not self._queue.empty():
                message = self._queue.get()
                logging.info("processing queue, message: %s", message)
