from rest_framework import serializers
from medias.models import Photo


class PhotoResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            "id",
            "file",
            "description",
            "room_id",
            "experience_id",
            "created_at",
            "updated_at",
        )
