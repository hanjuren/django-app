from django.db import models


class Experience(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    country = models.CharField(max_length=50, default="korea")
    city = models.CharField(max_length=80, default='seoul')
    price = models.PositiveIntegerField()
    address = models.CharField(max_length=250)
    started_at = models.TimeField()
    finished_at = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        "users.User",
        related_name="experiences",
        db_column="user_id",
        on_delete=models.CASCADE,
    )
    perks = models.ManyToManyField(
        "experiences.Perk",
        related_name="experiences",
        db_table="experience_perks",
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "experiences"


class Perk(models.Model):
    name = models.CharField(max_length=250)
    detail = models.CharField(max_length=250)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "perks"
