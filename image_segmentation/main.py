import logging
import os
import traceback

import pika
from config import config
from src.db.mongo.mongo_db_connector import MongoDBConnector
from src.image_segmentation.image_segmentation_model.segmentatin_model_factory import (
    SegmentationModelFactory,
)
from src.image_segmentation.visualisation.mask.mask_model import MaskModel
from src.queue.handler.message_handler import QueueBroker
from src.queue.rabbitmq.subscriber.rabbitmq_subscriber import RabbitMQSubscriber
from src.utils.download_model import download_file

logging.getLogger().setLevel(logging.INFO)


def main():
    db_connector = MongoDBConnector()
    logging.info("downloading segmentation model")
    os.makedirs("models", exist_ok=True)
    download_file(config["sam_segmentation_model_url"], config["sam_segmentation_model_path"])
    logging.info("downloaded segmentation model done")
    logging.info("starting subscriber")

    request_handler = QueueBroker(
        SegmentationModelFactory,
        MaskModel,
        {
            "sam_checkpoint": config["sam_segmentation_model_path"],
        },
        db_connector,
    )
    request_handler.start_consuming()

    try:
        subscriber = RabbitMQSubscriber(config["queue_name"], request_handler)
    except pika.exceptions.AMQPConnectionError:
        logging.error("failed to connect to rabbitmq")
        logging.error(traceback.format_exc())
        return
    subscriber.start_consuming()


if __name__ == "__main__":
    main()
