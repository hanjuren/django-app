from rest_framework import serializers
from reviews.models import Review


class ReviewsResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            "id",
            "payload",
            "rating",
            "user_id",
            "room_id",
            "experience_id",
            "created_at",
            "updated_at",
        )


class ReviewListResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    records = ReviewsResponseSerializer(many=True)
