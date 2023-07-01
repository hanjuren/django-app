from rest_framework import serializers
from experiences.models import Perk


class PerkCreationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=250)
    detail = serializers.CharField(max_length=250)
    description = serializers.CharField()

    def create(self, validated_data):
        return Perk.objects.create(**validated_data)
