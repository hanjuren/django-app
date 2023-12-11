from rest_framework import serializers

from users.models import User


class UserUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=10)
    gender = serializers.ChoiceField(
        choices=User.GenderChoices,
        required=False,
        allow_null=True,
    )
    language = serializers.ChoiceField(
        choices=User.LanguageChoices,
        required=False,
        allow_null=True,
    )
    currency = serializers.ChoiceField(
        choices=User.CurrencyChoices,
        required=False,
        allow_null=True,
    )


class UserAvatarUpdateSerializer(serializers.Serializer):
    file = serializers.ImageField(allow_null=True)
