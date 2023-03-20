import jwt
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from common.models import CommonModel


class User(AbstractUser, CommonModel):

    """User Definition"""

    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    class LanguageChoices(models.TextChoices):
        KR = ("kr", "Korea")
        EN = ("en", "English")

    class CurrencyChoices(models.TextChoices):
        WON = "won", "Korea Won"
        USD = "usd", "Dollar"

    email = models.CharField(
        max_length=100,
    )
    first_name = models.CharField(
        max_length=150,
        null=True,
    )
    last_name = models.CharField(
        max_length=150,
        null=True,
    )
    name = models.CharField(
        max_length=150,
        null=True,
    )
    is_host = models.BooleanField(
        default=False,
    )
    avatar = models.URLField(
        null=True,
    )
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
        null=True,
    )
    language = models.CharField(
        max_length=2,
        choices=LanguageChoices.choices,
        null=True,
    )
    currency = models.CharField(
        max_length=30,
        choices=CurrencyChoices.choices,
        null=True,
    )

    class Meta:
        db_table = "users"

    def gen_jwt_token(self):
        return jwt.encode(
            {"pk": self.pk},
            settings.SECRET_KEY,
            algorithm="HS256",
        )

