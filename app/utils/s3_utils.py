import boto3
import os
from app.logger import logger

S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")
S3_REGION_NAME = os.getenv("S3_REGION_NAME")

def download_file_from_s3(bucket: str, key: str, local_path: str):
    logger.info(f"Скачивание файла из S3: {bucket}/{key} → {local_path}")
    s3 = boto3.client(
        's3',
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY,
        endpoint_url=S3_ENDPOINT_URL,
        region_name=S3_REGION_NAME
    )
    try:
        s3.download_file(bucket, key, local_path)
        logger.info(f"Файл успешно скачан: {key}")
    except Exception as e:
        logger.error(f"Ошибка при скачивании {key} из S3: {e}")
        raise RuntimeError(f"Ошибка скачивания из S3: {e}")