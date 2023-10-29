import hashlib
import os
import uuid
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from config.s3 import PublicS3


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
    def generate_file_path(cls, file_name) -> str:
        base_dir = "photos/file"
        file_id = uuid.uuid4()
        file_name, extension = os.path.splitext(file_name)
        token = hashlib.md5(file_name.encode('utf-8')).hexdigest()

        return f"{base_dir}/{file_id}/{token[0:7]}{extension}"

    @classmethod
    def upload_image(cls, file) -> str:
        path = cls.generate_file_path(file.name)
        s3 = PublicS3()
        s3.put_object(path, file, file.content_type)

        return f"{settings.IMAGE_URL}/{path}"

    def delete_image(self) -> None:
        object_key = self.file.replace(f"{settings.IMAGE_URL}/", "")
        s3 = PublicS3()
        s3.delete_object(object_key)
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


@receiver(pre_delete, sender=Photo)
def pre_delete_handler(sender, instance, **kwargs):
    if instance.file:
        instance.delete_image()
