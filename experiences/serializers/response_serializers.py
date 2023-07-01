from rest_framework import serializers
from experiences.models import Perk


class PerkResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"
