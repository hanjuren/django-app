from rest_framework import serializers
from reviews.models import Review


class ReviewCreationSerializer(serializers.Serializer):
    payload = serializers.CharField()
    rating = serializers.IntegerField(min_value=0, max_value=5)

    def create(self, validated_data):
        return Review.objects.create(**validated_data)
