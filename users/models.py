import jwt
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(
            email,
            password=password,
            name=name
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    class LanguageChoices(models.TextChoices):
        KR = ("kr", "Korea")
        EN = ("en", "English")

    class CurrencyChoices(models.TextChoices):
        WON = ("won", "Korea Won")
        USD = ("usd", "Dollar")

    # columns
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=10)
    first_name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150, null=True)
    is_host = models.BooleanField(default=False)
    avatar = models.URLField(null=True)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices, null=True)
    language = models.CharField(max_length=2, choices=LanguageChoices.choices, null=True)
    currency = models.CharField(max_length=30, choices=CurrencyChoices.choices, null=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # methods
    def __str__(self) -> str:
        return self.name

    def generate_token(self):
        payload = {
            "user_id": self.id,
            "user_email": self.email,
            "user_name": self.name,
            "user_is_admin": self.is_admin,
            "iat": timezone.now(),
            "exp": timezone.now() + timezone.timedelta(hours=2)  # 2.hours
        }
        token = jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm="HS256",
        )

        return token

    @property
    def is_superuser(self):
        return self.is_admin

    class Meta:
        db_table = 'users'

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # user model 에서 사용할 고유 식별자
    REQUIRED_FIELDS = ['name']  # createsuperuser 커맨드를 실행하여 관리자를 생성할 때 입력받을 필드


@receiver(pre_delete, sender=User)
def pre_delete_handler(sender, instance, **kwargs):
    if instance.avatar:
        instance.delete_avatar()
