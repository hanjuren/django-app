from rest_framework import serializers
from .models import Wishlist
from rooms.serializers import RoomListSerializer


class WishListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wishlist
        fields = (
            "pk",
            "name",
            "rooms",
        )

    rooms = RoomListSerializer(many=True, read_only=True)
