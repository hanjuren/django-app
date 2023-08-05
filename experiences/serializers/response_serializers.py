from rest_framework import serializers
from experiences.models import Perk


class PerkResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"


class PerkListSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    records = PerkResponseSerializer(many=True)
