from django.db import models
from common.models import CommonModel
from django.conf import settings


class Experience(CommonModel):

    """Experience Model Definition"""

    name = models.CharField(
        max_length=250,
    )
    description = models.TextField()
    country = models.CharField(
        max_length=50,
        default="한국",
    )
    price = models.PositiveIntegerField()
    city = models.CharField(
        max_length=80,
        default="서울",
    )
    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    address = models.CharField(
        max_length=250,
    )
    starts_at = models.TimeField()
    ends_at = models.TimeField()
    perks = models.ManyToManyField(
        "experiences.Perk",
    )

    class Meta:
        db_table = "experiences"

    def __str__(self):
        return self.name


class Perk(CommonModel):

    """What is included on an Experiences"""

    name = models.CharField(
        max_length=100,
    )
    details = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )
    explanation = models.TextField(
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "perks"

    def __str__(self):
        return self.name
