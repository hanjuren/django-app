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

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class UserAvatarUpdateSerializer(serializers.Serializer):
    file = serializers.ImageField()

    def update(self, instance, validated_data):
        avatar = instance.upload_avatar(validated_data.get('file'))
        instance.avatar = avatar
        instance.save()

        return instance
