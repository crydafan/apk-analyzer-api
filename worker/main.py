"""
Worker
"""

import sys
import os
import json
import tempfile

from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from services.rabbitmq import RabbitMQ
from services import database
from services.s3 import S3

from lib.db import get_db

from enums import JobStatus


def main():
    """
    Main function to consume messages from RabbitMQ
    """
    rabbitmq = RabbitMQ()
    rabbitmq.declare_queue("job_queue")

    s3 = S3()

    db = next(get_db())

    def message_callback(
        _channel: BlockingChannel,
        method: Basic.Deliver,
        _properties: BasicProperties,
        body: bytes,
    ):
        metadata = json.loads(body)

        key = metadata.get("key") or ""
        job = metadata.get("job") or ""

        print(f"Received message: {metadata}")

        database.update_job(
            db=db,
            job_id=job,
            status=JobStatus.IN_PROGRESS,
        )

        with tempfile.NamedTemporaryFile() as file:
            s3.download_fileobject(key, file)

        print(f"Processed file for job {job}")

        database.update_job(
            db=db,
            job_id=job,
            status=JobStatus.COMPLETED,
        )

        if method.delivery_tag is not None:
            rabbitmq.acknowledge_message(delivery_tag=method.delivery_tag)

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
