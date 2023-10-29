from rest_framework import serializers

from bookings.models import Booking
from rooms.serializers import RoomResponseSerializer


class PublicBookingsResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "id",
            "kind",
            "check_in_at",
            "check_out_at",
            "guests",
            "created_at",
            "updated_at",
        )


class PublicBookingListResponseSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    records = PublicBookingsResponseSerializer(many=True)


class PublicRoomBookingResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "id",
            "kind",
            "check_in_at",
            "check_out_at",
            "guests",
            "created_at",
            "updated_at",
        )
