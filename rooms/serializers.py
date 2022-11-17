from rest_framework.serializers import ModelSerializer
from rooms.models import Amenity, Room
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer


class RoomListSerializer(ModelSerializer):

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
        )


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "pk",
            "name",
            "description",
            "created_at"
        )


class RoomDeatilSerializer(ModelSerializer):

    owner = TinyUserSerializer(read_only=True)
    amenities = AmenitySerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Room
        fields = "__all__"
