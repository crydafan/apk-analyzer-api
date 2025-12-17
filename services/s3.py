"""
S3 service module
"""

import os
from typing import IO

import boto3
from mypy_boto3_s3 import S3Client


class S3:
    """
    S3 service class for handling file operations
    """

    s3_client: S3Client

    def __init__(self):
        self.bucket_name = os.getenv("S3_BUCKET_NAME") or ""

        access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        default_region = os.getenv("AWS_DEFAULT_REGION")

        endpoint_url = os.getenv("AWS_ENDPOINT_URL")

        session = boto3.Session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name=default_region,
        )

        self.s3_client = session.client(
            "s3", region_name=default_region, endpoint_url=endpoint_url
        )

    def upload_object(self, key: str, body: bytes):
        """
        Upload a file to an S3 bucket
        """
        self.s3_client.put_object(Bucket=self.bucket_name, Key=key, Body=body)

    def download_fileobject(self, key: str, file: IO[bytes]):
        """
        Download a file object from an S3 bucket
        """
        self.s3_client.download_fileobj(Bucket=self.bucket_name, Key=key, Fileobj=file)
