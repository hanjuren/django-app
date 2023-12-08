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

    def create(self, validated_data):
        user = User(
            email=validated_data.get('email'),
            name=validated_data.get('name'),
            gender=validated_data.get('gender'),
            language=validated_data.get('language'),
            currency=validated_data.get('currency'),
            is_host=validated_data.get('is_host')
        )
        user.set_password(validated_data.get('password'))
        user.save()
        return user

    class Meta:
        validators = [UniqueTogetherValidator(queryset=User.objects.all(), fields=['email'])]


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, data):
        request = self.context.get('request')
        old_password = data.get('old_password')
        if request.user.check_password(old_password) is False:
            raise exceptions.ValidationError({'old_password': 'The old password is not valid.'})

        return data

    def update(self, instance, validated_data):
        new_password = validated_data.get('new_password')
        instance.set_password(new_password)
        instance.save()

        return instance


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
