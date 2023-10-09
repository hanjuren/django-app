from rest_framework import serializers
from rooms.models import Room, Amenity
from users.serializers import TinyUserSerializer
from categories.serializers import CategoryResponseSerializer
from reviews.serializers import ReviewsResponseSerializer
from medias.serializers import PhotoResponseSerializer


class AmenityResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = "__all__"


class AmenityListResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    records = AmenityResponseSerializer(many=True)


class RoomsResponseSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    photos = PhotoResponseSerializer(many=True)

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
            "photos",
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
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    photos = PhotoResponseSerializer(many=True)
    is_liked = serializers.SerializerMethodField()

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
            "photos",
            "is_liked",
        )

    def get_rating(self, room):
        return room.reviews_rating()

    def get_is_owner(self, room):
        request = self.context.get("request", {})
        return request.user.id == room.user_id

    def get_is_liked(self, room):
        request = self.context.get("request", {})
        if request.user.id:
            return room.wishlists.filter(user_id=request.user.id).exists()
        else:
            return False


class RoomListResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    records = RoomsResponseSerializer(many=True)
