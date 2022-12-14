from django.db import models
from common.models import CommonModel


class Photo(CommonModel):

    """Photo Model Definition"""

    file = models.URLField()
    description = models.CharField(
        max_length=140,
        null=True,
        blank=True,
    )
    room = models.ForeignKey(
        "rooms.Room",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="photos",
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="photos",
    )

    class Meta:
        db_table = 'photos'

    def __str__(self):
        return f"Photo File {self.id}"


class Video(CommonModel):

    """Video Model definition"""

    file = models.URLField()
    experience = models.OneToOneField(
        "experiences.Experience",
        on_delete=models.CASCADE,
        related_name="video",
    )

    class Meta:
        db_table = "videos"

    def __str__(self):
        return f"Video File {self.id}"
