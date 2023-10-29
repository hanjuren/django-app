from rest_framework import serializers
from users.models import User


class TinyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "name",
            "avatar",
            "created_at",
            "updated_at",
        )

class PrivateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)
