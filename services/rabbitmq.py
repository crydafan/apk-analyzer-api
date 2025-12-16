"""
RabbitMQ service module
"""

import os
import json
import pika


class RabbitMQ:
    """
    RabbitMQ service class
    """

    def __init__(self):
        rabbitmq_url = (
            os.getenv("RABBBITMQ_URL") or "amqp://guest:guest@localhost:5672/"
        )
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
