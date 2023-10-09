from rest_framework import serializers
from wishlists.models import Wishlist
from rooms.serializers import RoomsResponseSerializer


class WishlistsResponseSerializer(serializers.ModelSerializer):
    rooms = RoomsResponseSerializer(many=True)

    class Meta:
        model = Wishlist
        fields = (
            "id",
            "name",
            "user_id",
            "rooms",
            "created_at",
            "updated_at",
        )

class WishlistListResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    records = WishlistsResponseSerializer(many=True)
