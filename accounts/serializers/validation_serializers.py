from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueTogetherValidator

from users.models import User

class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField()
    name = serializers.CharField(max_length=10)
    gender = serializers.ChoiceField(choices=User.GenderChoices)
    language = serializers.ChoiceField(choices=User.LanguageChoices)
    currency = serializers.ChoiceField(choices=User.CurrencyChoices)
    is_host = serializers.BooleanField(default=False)

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['email'],
            )
        ]


class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
