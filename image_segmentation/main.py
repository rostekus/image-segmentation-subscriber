import logging

from config import config
from src.queue.handler.message_handler import QueueBroker
from src.queue.rabbitmq.subscriber.rabbitmq_subscriber import RabbitMQSubscriber
from src.image_segmentation.image_segmentation_model.segmentatin_model_factory import SegmentationModelFactory
logging.getLogger().setLevel(logging.INFO)

def main():
    logging.info("starting subscriber")
    request_handler = QueueBroker(SegmentationModelFactory)
    subscriber = RabbitMQSubscriber(config["queue_name"], request_handler)
    subscriber.start_consuming()


if __name__ == "__main__":
    main()
