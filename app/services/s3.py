import uuid
from typing import Optional

import aioboto3
from botocore.exceptions import ClientError

from app.core.config import settings


class S3Service:

    class FileType(str):
        DROP = "drop"
        COVER = "cover"

    FILE_VALIDATION = {
        FileType.DROP: {"extensions": ["mp3", "aac"], "max_size": settings.MAX_DROP_SIZE},
        FileType.COVER: {"extensions": ["png", "jpg", "jpeg"], "max_size": settings.MAX_COVER_SIZE},
    }

    def __init__(self):
        self.session = aioboto3.Session()
        self.bucket_name = settings.S3_BUCKET_NAME
        self.s3_url = settings.S3_ENDPOINT_URL

    @staticmethod
    def generate_key(user_id: uuid.UUID, drop_id: uuid.UUID, file_type: str, file_name: str) -> str:
        ext = file_name.split('.')[-1]
        return f"artists/{user_id}/drops/{drop_id}/{file_type}.{ext}"

    def validate_file(self, file, file_type: str):
        valid = self.FILE_VALIDATION.get(file_type)
        if not valid:
            raise ValueError(f"Unsupported file type: {file_type}")

        ext = file.filename.split('.')[-1].lower()
        if ext not in valid["extensions"]:
            raise ValueError(f"Invalid file extension '{ext}' for type {file_type}")

        file.file.seek(0, 2)
        size = file.file.tell()
        file.file.seek(0)

        if size > valid["max_size"]:
            raise ValueError(f"File size {size} exceeds max for type {file_type}")

    async def upload_file(
        self, file, content_type: str, key: str, file_type: Optional[str] = None
    ) -> str:
        if file_type:
            self.validate_file(file, file_type)

        try:
            async with self.session.client(
                "s3",
                region_name=settings.S3_REGION_NAME,
                aws_access_key_id=settings.S3_ACCESS_KEY,
                aws_secret_access_key=settings.S3_SECRET_KEY,
                endpoint_url=settings.S3_ENDPOINT_URL,
            ) as s3:
                await s3.upload_fileobj(
                    Fileobj=file,
                    Bucket=self.bucket_name,
                    Key=key,
                    ExtraArgs={"ContentType": content_type, "ACL": "public-read"},
                )
            return f"{self.s3_url}/{self.bucket_name}/{key}"
        except ClientError as e:
            raise RuntimeError(f"S3 upload failed: {e}")

    async def delete_file(self, key: str) -> None:
        async with self.session.client(
            "s3",
            region_name=settings.S3_REGION_NAME,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            endpoint_url=settings.S3_ENDPOINT_URL,
        ) as s3:
            try:
                await s3.delete_object(Bucket=self.bucket_name, Key=key)
            except ClientError:
                pass

    async def drop_upload(self, file, user_id: uuid.UUID, drop_id: uuid.UUID) -> str:
        key = self.generate_key(user_id, drop_id, self.FileType.DROP, file.filename)
        return await self.upload_file(
            file, content_type="audio/mpeg", key=key, file_type=self.FileType.DROP
        )

    async def cover_upload(self, file, user_id: uuid.UUID, drop_id: uuid.UUID) -> str:
        key = self.generate_key(user_id, drop_id, self.FileType.COVER, file.filename)
        return await self.upload_file(
            file, content_type="image/png", key=key, file_type=self.FileType.COVER
        )
