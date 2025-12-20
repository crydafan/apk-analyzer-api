"""
RabbitMQ service module
"""

import os
import json
from collections.abc import Callable

import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties


class RabbitMQ:
    """
    RabbitMQ service class
    """

    def __init__(self):
        rabbitmq_url = os.getenv("RABBITMQ_URL") or "amqp://guest:guest@localhost:5672/"
        self.connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
        self.channel = self.connection.channel()

    def declare_queue(self, queue_name: str):
        """
        Declare a RabbitMQ queue
        """

        # TODO: Make durable True in production
        self.channel.queue_declare(queue=queue_name, durable=False)

    def publish_message(self, queue: str, message: dict[str, object]):
        """
        Publish a message to a RabbitMQ queue
        """
        self.channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2),
        )

    def consume_messages(
        self,
        queue: str,
        callback: Callable[
            [BlockingChannel, Basic.Deliver, BasicProperties, bytes], None
        ],
    ):
        """
        Consume messages from a RabbitMQ queue
        """
        self.channel.basic_consume(
            queue=queue, on_message_callback=callback, auto_ack=False
        )
        self.channel.start_consuming()

    def acknowledge_message(self, delivery_tag: int):
        """
        Acknowledge a message
        """
        self.channel.basic_ack(delivery_tag=delivery_tag)
