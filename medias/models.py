import hashlib
import os
import boto3
import uuid
from django.conf import settings
from django.db import models


class Photo(models.Model):
    file = models.URLField()
    description = models.CharField(max_length=150)
    room = models.ForeignKey(
        "rooms.Room",
        related_name="photos",
        db_column='room_id',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        related_name="photos",
        db_column="experience_id",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def initialize_s3_resource(cls):
        access_key = settings.AWS_S3_ACCESS_KEY_ID
        secret_access_key = settings.AWS_S3_SECRET_ACCESS_KEY

        s3 = boto3.resource(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_access_key
        )

        return s3


    @classmethod
    def generate_file_path(cls, file_name) -> str:
        base_dir = "photos/file"
        file_id = uuid.uuid4()
        file_name, extension = os.path.splitext(file_name)
        token = hashlib.md5(file_name.encode('utf-8')).hexdigest()

        return f"{base_dir}/{file_id}/{token[0:7]}{extension}"

    @classmethod
    def upload_image(cls, file) -> str:
        s3 = cls.initialize_s3_resource()
        bucket = s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)

        path = cls.generate_file_path(file.name)
        bucket.put_object(
            Key=path,
            Body=file,
            ContentType=file.content_type,
        )

        return f"{settings.IMAGE_URL}/{path}"

    @classmethod
    def delete_image(cls, object_key: str) -> None:
        s3 = Photo.initialize_s3_resource()
        s3.Object(
            settings.AWS_STORAGE_BUCKET_NAME,
            object_key,
        ).delete()

        return

    def __str__(self) -> str:
        return "Photo file"

    class Meta:
        db_table = "photos"


class Video(models.Model):
    file = models.FileField()
    experience = models.ForeignKey(
        "experiences.Experience",
        related_name="videos",
        db_column="experience_id",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return "Video file"

    class Meta:
        db_table = "videos"
