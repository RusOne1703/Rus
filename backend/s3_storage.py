import boto3
from botocore.exceptions import NoCredentialsError
import os

S3_ENDPOINT = os.getenv("S3_ENDPOINT", "https://s3.yandexcloud.net")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY", "your_access_key")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY", "your_secret_key")
S3_BUCKET = os.getenv("S3_BUCKET", "sotrue-images")

# Инициализация S3 клиента (Yandex Object Storage / AWS S3)
s3_client = boto3.client(
    's3',
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY
)

def upload_image_to_s3(file_path: str, object_name: str) -> str:
    """
    Загружает изображение с локального диска в S3 и возвращает публичный URL.
    """
    try:
        s3_client.upload_file(
            file_path,
            S3_BUCKET,
            object_name,
            ExtraArgs={'ACL': 'public-read', 'ContentType': 'image/jpeg'}
        )
        url = f"{S3_ENDPOINT}/{S3_BUCKET}/{object_name}"
        return url
    except FileNotFoundError:
        print("Файл не найден")
        return None
    except NoCredentialsError:
        print("Неверные учетные данные S3")
        return None
