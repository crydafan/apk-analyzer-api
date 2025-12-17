"""
Worker
"""

import sys
import os
import json

from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from services.rabbitmq import RabbitMQ


def main():
    """
    Main function to consume messages from RabbitMQ
    """
    rabbitmq = RabbitMQ()
    rabbitmq.declare_queue("job_queue")

    def message_callback(
        _channel: BlockingChannel,
        _method: Basic.Deliver,
        _properties: BasicProperties,
        body: bytes,
    ):
        metadata = json.loads(body)
        print(f"Received message: {metadata}")

    print("Worker started, waiting for messages")

    rabbitmq.consume_messages(
        "job_queue",
        callback=message_callback,
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted by user")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
