import logging
import os

import pika
from src.queue.handler.handler_protocol import IHandler

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class RabbitMQSubscriber:
    def __init__(self, queue_name: str, message_handler: IHandler):
        self.queue_name = queue_name
        self.message_handler = message_handler
        self.connection = None
        self.channel = None
        host = os.environ.get("RABBITMQ_HOST", "localhost")
        port = os.environ.get("RABBITMQ_PORT", 5672)
        username = os.environ.get("RABBBITMQ_USERNAME")
        password = os.environ.get("RABBITMQ_PASSWORD")
        self._connect(host, port, username, password)

    def _connect(
        self,
        host: str = "localhost",
        port: str = 5672,
        username: str = "guest",
        password: str = "guest",
    ) -> None:
        credentials = pika.PlainCredentials(username, password)
        parameters = pika.ConnectionParameters(host=host, port=port, credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name)

    def start_consuming(self) -> None:
        if self.channel is None:
            raise RuntimeError("Subscriber is not connected")
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.request_handler.regiser,
            auto_ack=True,
        )
        logger.info("Waiting for messages...")
        self.channel.start_consuming()
