import os
import uuid
from abc import ABC, abstractmethod

import boto3
from dotenv import load_dotenv
from fastapi import UploadFile

load_dotenv()


class Storage(ABC):
    @abstractmethod
    def save(self, file: UploadFile) -> str:
        raise NotImplementedError


class LocalStorage(Storage):
    def __init__(self) -> None:
        self.upload_dir = os.getenv("UPLOAD_DIR", "uploads")
        os.makedirs(self.upload_dir, exist_ok=True)

    def save(self, file: UploadFile) -> str:
        nome = f"{uuid.uuid4().hex}_{file.filename}"
        caminho = os.path.join(self.upload_dir, nome)
        with open(caminho, "wb") as destino:
            destino.write(file.file.read())
        return f"/{self.upload_dir}/{nome}"


class S3Storage(Storage):
    def __init__(self) -> None:
        self.bucket = os.getenv("AWS_S3_BUCKET")
        self.region = os.getenv("AWS_REGION")
        self.client = boto3.client(
            "s3",
            region_name=self.region,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", None),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", None),
            aws_session_token=os.getenv("AWS_SESSION_TOKEN", None),
        )

    def save(self, file: UploadFile) -> str:
        chave = f"{uuid.uuid4().hex}_{file.filename}"
        self.client.upload_fileobj(file.file, self.bucket, chave)
        return f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{chave}"


def get_storage() -> Storage:
    if os.getenv("STORAGE_BACKEND", "local").lower() == "s3":
        return S3Storage()
    return LocalStorage()
