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

    email = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=30, null=True)
    first_name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150, null=True)
    name = models.CharField(max_length=150, null=True)
    is_host = models.BooleanField(default=False)
    avatar = models.URLField(null=True)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices, null=True)
    language = models.CharField(max_length=2, choices=LanguageChoices.choices, null=True)
    currency = models.CharField(max_length=30, choices=CurrencyChoices.choices, null=True)

    class Meta:
        db_table = "users"

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"<User id: {self.id}, email: {self.email}>"

    def gen_jwt_token(self):
        return jwt.encode(
            {"pk": self.pk},
            settings.SECRET_KEY,
            algorithm="HS256",
        )
