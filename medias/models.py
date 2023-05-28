from django.db import models


class Photo(models.Model):
    file = models.ImageField()
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

    def __str__(self) -> str:
        return  "Photo file"

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
