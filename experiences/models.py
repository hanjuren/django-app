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
        related_name="experiences",
    )
    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="experiences",
    )

    class Meta:
        db_table = "experiences"

    def __str__(self):
        return self.name

    def add_perks(self, perk_ids):
        perks = Perk.objects.filter(pk__in=perk_ids)
        self.perks.clear()
        for perk in perks:
            self.perks.add(perk)


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
