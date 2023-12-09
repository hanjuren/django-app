from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueTogetherValidator
from users.models import User

class UserCreationSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField()
    name = serializers.CharField(max_length=10)
    gender = serializers.ChoiceField(choices=User.GenderChoices)
    language = serializers.ChoiceField(choices=User.LanguageChoices)
    currency = serializers.ChoiceField(choices=User.CurrencyChoices)
    is_host = serializers.BooleanField(default=False)

    class Meta:
        validators = [UniqueTogetherValidator(queryset=User.objects.all(), fields=['email'])]


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, data):
        user = self.context.get('user')
        old_password = data.get('old_password')
        if user.check_password(old_password) is False:
            raise exceptions.ValidationError({'old_password': 'The old password is not valid.'})

        return data


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
