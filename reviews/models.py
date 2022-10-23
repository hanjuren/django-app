from django.db import models
from common.models import CommonModel
from django.conf import settings
from django.core.validators import MaxValueValidator


class Review(CommonModel):

    """Review Model Definition"""

    payload = models.TextField()
    rating = models.PositiveIntegerField(
        validators=[MaxValueValidator(5)]
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        db_column="user_id",
    )
    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "reviews"

    def __str__(self):
        return f"{self.user} / {self.rating}"
