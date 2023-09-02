from rest_framework import serializers, exceptions
from rooms.models import Room, Amenity
from categories.models import Category


class AmenityCreationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
    description = serializers.CharField(
        max_length=150,
        required=False,
        allow_null=True,
    )

    def create(self, validated_data):
        return Amenity.objects.create(**validated_data)


class AmenityUpdateSerializer(AmenityCreationSerializer):
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class RoomCreationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=250)
    country = serializers.CharField(max_length=250, default="korea")
    city = serializers.CharField(max_length=80, default="seoul")
    price = serializers.IntegerField()
    rooms = serializers.IntegerField()
    toilets = serializers.IntegerField()
    description = serializers.CharField(allow_null=True)
    address = serializers.CharField(max_length=250)
    pet_friendly = serializers.BooleanField(default=False)
    kind = serializers.ChoiceField(choices=Room.KindChoices)
    category_id = serializers.IntegerField()

    def validate(self, data):
        category_id = data.get("category_id")
        category = Category.objects.get(id=category_id)
        if category.kind != 'rooms':
            raise exceptions.ParseError("The Category kind should be 'rooms'")

        return data

    def create(self, validated_data):
        return Room.objects.create(**validated_data)


class RoomUpdateSerializer(RoomCreationSerializer):
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
