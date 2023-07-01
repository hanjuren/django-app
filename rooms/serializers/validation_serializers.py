from rest_framework import serializers
from rooms.models import Amenity


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
