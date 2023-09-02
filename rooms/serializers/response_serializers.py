from rest_framework import serializers
from rooms.models import Room, Amenity
from users.serializers import TinyUserSerializer
from categories.serializers import CategoryResponseSerializer


class AmenityResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = "__all__"


class AmenityListResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    records = AmenityResponseSerializer(many=True)


class RoomsResponseSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()  # N+1 query
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = (
            "id",
            "name",
            "country",
            "city",
            "price",
            "user_id",
            "created_at",
            "updated_at",
            "rating",
            "is_owner",
        )

    def get_rating(self, room):
        return room.reviews_rating()

    def get_is_owner(self, room):
        request = self.context.get("request", {})
        return request.user.id == room.user_id


class RoomResponseSerializer(serializers.ModelSerializer):
    user = TinyUserSerializer()
    amenities = AmenityResponseSerializer(many=True)
    category = CategoryResponseSerializer()
    rating = serializers.SerializerMethodField()  # N+1 query
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = (
            "id",
            "name",
            "country",
            "city",
            "price",
            "rooms",
            "toilets",
            "description",
            "address",
            "pet_friendly",
            "kind",
            "user_id",
            "category_id",
            "created_at",
            "updated_at",
            "user",
            "amenities",
            "category",
            "rating",
            "is_owner",
        )

    def get_rating(self, room):
        return room.reviews_rating()

    def get_is_owner(self, room):
        request = self.context.get("request", {})
        return request.user.id == room.user_id


class RoomListResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    records = RoomsResponseSerializer(many=True)
