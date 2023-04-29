import logging
import os

import pika
from src.queue.queue_protocols import AbstractHandler, IHandler


class RabbitMQPublisher(AbstractHandler):
    def __init__(self, queue_name: str):
        self.queue_name = queue_name
        self.connection = None
        self.channel = None
        host = os.environ.get("RABBITMQ_HOST", "localhost")
        port = int(os.environ.get("RABBITMQ_PORT", 5672))
        username = os.environ["RABBITMQ_USERNAME"]
        password = os.environ["RABBITMQ_PASSWORD"]
        self._connect(host, port, username, password)

    def _connect(
        self,
        host: str = "localhost",
        port: int = 5672,
        username: str = "guest",
        password: str = "guest",
    ) -> None:
        credentials = pika.PlainCredentials(username, password)
        parameters = pika.ConnectionParameters(host=host, port=port, credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)

        if self.connection is None:
            raise RuntimeError("Failed to connect to RabbitMQ")

        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name)

    def register(self, message: bytes) -> None:
        return self.publish_message(message)

    def publish_message(self, message: bytes) -> None:
        if self.channel is None:
            raise RuntimeError("Publisher is not connected")
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue_name,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2),
        )
