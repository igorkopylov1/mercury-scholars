import logging
import typing as tp
import json
import asyncio
import aioboto3
from botocore.exceptions import ClientError

import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BucketStatus:
    EXIST = True
    NOT_EXIST = False


class FileStatus:
    EXIST = True
    NOT_EXIST = False


class S3Manager:
    ENDPOINT_URL = "https://storage.yandexcloud.net"
    MAX_CONTENT_HISTORY = 6

    async def _is_file_exist(self, s3client: aioboto3.Session.client, bucket_name: str, key: str) -> bool:
        try:
            await s3client.head_object(Bucket=bucket_name, Key=key)
            return FileStatus.EXIST
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                logger.info(f"File '{key}' does not exist in bucket '{bucket_name}'.")
                return FileStatus.NOT_EXIST
            else:
                logger.error(f"Error checking existence of file '{key}' in bucket '{bucket_name}': {e}")
                return FileStatus.NOT_EXIST

    async def _is_bucket_exist(self, s3client: aioboto3.Session.client, bucket_name: str) -> bool:
        try:
            await s3client.head_bucket(Bucket=bucket_name)
            return BucketStatus.EXIST
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return BucketStatus.NOT_EXIST
            logger.error(f"Error checking bucket existence: {e}")
            return False

    async def create_bucket(self, session: aioboto3.Session, bucket_name: str) -> None:
        async with session.client(
            service_name='s3',
            endpoint_url=self.ENDPOINT_URL
        ) as s3client:
            if not await self._is_bucket_exist(s3client, bucket_name):
                try:
                    await s3client.create_bucket(Bucket=bucket_name)
                    logger.info(f"Bucket '{bucket_name}' created successfully.")
                except ClientError as e:
                    if e.response['Error']['Code'] == '403':
                        logger.warning(f"Bucket '{bucket_name}' exists but you do not have access.")
                    else:
                        logger.error(f"Unexpected error while creating bucket: {e}")

    async def read_file(self, session: aioboto3.Session, bucket_name: str, key: str) -> tp.Optional[list[dict]]:  # TODO: json format
        async with session.client(
            service_name='s3',
            endpoint_url=self.ENDPOINT_URL
        ) as s3client:
            if not await self._is_file_exist(s3client, bucket_name, key):
                logger.warning(f"File '{bucket_name}' does not exist.")
                return None

            try:
                history_object_response = await s3client.get_object(
                    Bucket=bucket_name, Key=key
                )
                response_object = await history_object_response["Body"].read()
                #return response_object.decode('utf-8')
                return json.loads(response_object)

            except ClientError as e:
                logger.error(f"Error retrieving object '{key}' from bucket '{bucket_name}': {e}")
                return None
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")
                return None
    
    @staticmethod
    async def add_ai_content(content: list[dict], future: asyncio.Future) -> None:
        ai_response = await future
        content.append({"role": "assistant", "content": ai_response})
    
    @classmethod
    def del_usless_content(cls, content: list[dict]) -> None:
        if len(content) >= cls.MAX_CONTENT_HISTORY:
            del content[:len(content) - cls.MAX_CONTENT_HISTORY + 1]


    async def write_file(self, session: aioboto3.Session, bucket_name: str, key: str, content: list[dict], *, future: tp.Optional[asyncio.Future] = None) -> None:  # TODO: json format
        async with session.client(
            service_name='s3',
            endpoint_url=self.ENDPOINT_URL
        ) as s3client:
            try:
                if future:
                    await self.add_ai_content(content=content, future=future)
                self.del_usless_content(content)
                dump_content = json.dumps(content)
                await s3client.put_object(Bucket=bucket_name, Key=key, Body=dump_content)
                logger.info(f"File '{key}' successfully written to bucket '{bucket_name}'.")
            except ClientError as e:
                logger.error(f"Failed to write file '{key}' to bucket '{bucket_name}': {e}")
            except Exception as e:
                logger.error(f"An unexpected error occurred while writing file '{key}': {e}")
