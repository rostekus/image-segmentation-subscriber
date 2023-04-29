import json
import logging
import traceback
from multiprocessing import Process, Queue
from typing import Type

import numpy as np
from src.db.db_protocol import DBConnection
from src.image_segmentation.image_segmentation_model.segmentatin_model_factory import (
    SegmentationModelFactory,
)
from src.image_segmentation.visualisation.effects_model_protocol import EffectsModel
from src.queue.queue_protocols import AbstractHandler

logging.getLogger().setLevel(logging.INFO)


class SingletonMeta(type):
    _instances: dict[Type["SingletonMeta"], "SingletonMeta"] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class QueueBroker(AbstractHandler, metaclass=SingletonMeta):
    def __init__(
        self,
        image_segmentation_factory: SegmentationModelFactory,
        visualization_model: EffectsModel,
        segmentation_model_kwargs: dict,
        db_connector: DBConnection,
    ):
        self._queue: Queue = Queue()
        self._image_segmentation_factory = image_segmentation_factory
        self._visualization_model = visualization_model
        self._segmentation_model_kwargs = segmentation_model_kwargs
        self.db_connector = db_connector

    def register(self, message: bytes) -> None:
        try:
            logging.info("registering message: %s", message)
            message = json.loads(message)
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            logging.error(f"message is not a valid json. {message!r}. error: {e}")
            return
        self._queue.put(message)
        # invoke next handler
        return super().register(message)

    @staticmethod
    def _processing_queue(
        queue,
        segmentation_model_factory: SegmentationModelFactory,
        visualization_model: EffectsModel,
        segmentation_model_kwargs: dict,
        db_connector: DBConnection,
    ):
        while True:
            if not queue.empty():
                try:
                    message = queue.get()
                    logging.info("processing queue, message: %s", message)

                    model_name = message.get("model_name")
                    image_id = message.get("imageID")

                    logging.info(f"downloading pic {image_id} from db")
                    with db_connector:
                        image_bytes = db_connector.download_file(image_id)
                    image = np.frombuffer(image_bytes, dtype=np.uint8)
                    logging.info(f"downloaded pic {image_id} from db")

                    logging.info(f"segmenting image using {model_name}")
                    segmentation_model = segmentation_model_factory.get_model(model_name, **segmentation_model_kwargs)
                    masks = segmentation_model.process(image)
                    output_img = visualization_model.add_effect(image, masks)
                    logging.info(f"segmented image using {model_name}")

                    logging.info(f"uploading image {image_id} to db")
                    with db_connector:
                        db_connector.upload_file("image_id", output_img.tobytes())
                    logging.info(f"uploaded image {image_id} to db")

                    logging.info("finished processing message: %s", message)
                except Exception as e:
                    exception = traceback.format_exc() + str(e)
                    logging.error(exception)

    def start_consuming(self):
        logging.info("starting consuming")
        p = Process(
            target=self._processing_queue,
            args=(
                self._queue,
                self._image_segmentation_factory,
                self._visualization_model,
                self._segmentation_model_kwargs,
                self.db_connector,
            ),
        )
        p.start()
