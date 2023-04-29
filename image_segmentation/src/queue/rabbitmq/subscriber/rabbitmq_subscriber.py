import logging
import os

import pika
from src.queue.queue_protocols import IHandler


class RabbitMQSubscriber:
    """This class represents a RabbitMQ subscriber, which connects to a RabbitMQ server
    and listens for messages on a specific queue. When a message is received,
     it calls a message handler to process the message.

    Attributes:
        queue_name (str): The name of the queue to listen on.
        message_handler (IHandler): An object that implements the `IHandler` interface,
        which defines a `register` method that will be called to process each message.
        connection (pika.BlockingConnection): The connection to the RabbitMQ server.
        channel (pika.channel.Channel): The channel used to communicate with the RabbitMQ server.

    Methods:
        __init__(queue_name: str, message_handler: IHandler) -> None:
            Initializes the `RabbitMQSubscriber` object and connects to the RabbitMQ server.
        _connect(host: str = "localhost", port: int = 5672, username: str = "guest", password: str = "guest") -> None:
            Connects to the RabbitMQ server.
        _callback_wrapper(ch: pika.channel.Channel,
        method: pika.spec.Basic.Deliver, properties: pika.spec.BasicProperties, body: bytes) -> None:
            Wraps the message handler's `register` method and passes the received message to it.
        start_consuming() -> None:
            Begins consuming messages from the queue, calling the message handler's `register` method for each message."""

    def __init__(self, queue_name: str, message_handler: IHandler):
        self.queue_name = queue_name
        self.message_handler = message_handler
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

    def _callback_wrapper(
        self, ch: pika.channel.Channel, method: pika.spec.Basic.Deliver, properties: pika.spec.BasicProperties, body: bytes
    ) -> None:
        logging.info(f"Received message {body!r}")
        self.message_handler.register(body)

    def start_consuming(self) -> None:
        if self.channel is None:
            raise RuntimeError("Subscriber is not connected")
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self._callback_wrapper,
            auto_ack=True,
        )
        while True:
            try:
                self.channel.start_consuming()
            except Exception as e:
                logging.error(e)
