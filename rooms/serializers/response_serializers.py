from rest_framework import serializers
from rooms.models import Amenity


class AmenityResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = "__all__"
