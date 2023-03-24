from rest_framework.serializers import ModelSerializer
from .models import User


class SignUpSerializer(ModelSerializer):
    """
    유저 생성
    """

    class Meta:
        model = User
        fields = (
            "pk",
            "email",
            "password",
        )


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "pk",
            "email",
            "name",
            "is_active",
            "first_name",
            "last_name",
            "is_host",
            "avatar",
            "gender",
            "language",
            "currency",
            "created_at",
            "updated_at",
        )


class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "pk",
            "name",
            "avatar",
            "username",
        )


class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "id",
            "password",
            "is_superuser",
            "is_staff",
            "is_active",
            "first_name",
            "last_name",
            "groups",
            "user_permissions",
        )
