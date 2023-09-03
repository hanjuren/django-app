from rest_framework import serializers
from medias.models import Photo


class PhotoCreationSerializer(serializers.Serializer):
    file = serializers.ImageField()
    description = serializers.CharField(max_length=150)

    def create(self, validated_data):
        file = validated_data.get('file')
        validated_data['file'] = Photo.upload_image(file)

        return Photo.objects.create(**validated_data)
