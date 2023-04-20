import json
import traceback
import logging
from typing import Type
from multiprocessing import Process, Queue
from src.image_segmentation.image_segmentation_model.segmentatin_model_factory import (
    SegmentationModelFactory,
)


from src.image_segmentation.visualisation.effects_model_protocol import EffectsModel

logging.getLogger().setLevel(logging.INFO)


class SingletonMeta(type):
    _instances: dict[Type["SingletonMeta"], "SingletonMeta"] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class QueueBroker(metaclass=SingletonMeta):
    def __init__(self, image_segmentation_factory: SegmentationModelFactory,
                 visualization_model: EffectsModel):
        self._queue: Queue = Queue()
        self._image_segmentation_factory = image_segmentation_factory
        self._visualization_model = visualization_model

    def register(self, message: bytes) -> None:
        try:
            logging.info("registering message: %s", message)
            message = json.loads(message)
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            logging.error(
                f"message is not a valid json. {message!r}. error: {e}")
            return
        self._queue.put(message)

    @staticmethod
    def _processing_queue(queue, segmentation_model_factory: SegmentationModelFactory, visualization_model: EffectsModel):
        while True:
            if not queue.empty():
                try:
                    message = queue.get()
                    model_name = message.get("model")
                    image = message.get("image")
                    segmentation_model = segmentation_model_factory.get_model(
                        model_name)
                    masks = segmentation_model.process(image)
                    output_img = visualization_model.process(image, masks)
                    logging.info("processing queue, message: %s", message)
                except Exception as e:
                    exception = traceback.format_exc() + str(e)
                    logging.error(exception)

    def start_consuming(self):
        logging.info("starting consuming")
        p = Process(target=self._processing_queue,
                    args=(self._queue, self._image_segmentation_factory,
                          self._visualization_model))
        p.start()
