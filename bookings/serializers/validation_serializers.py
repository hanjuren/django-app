from django.utils import timezone
from rest_framework import serializers, exceptions
from bookings.models import Booking


class RoomBookingCreationSerializer(serializers.Serializer):
    kind = serializers.ChoiceField(choices=Booking.BookingKindChoices)
    check_in_at = serializers.DateField()
    check_out_at = serializers.DateField()
    guests = serializers.IntegerField(min_value=1)

    def validate_kind(self, value):
        if value != "room":
            raise serializers.ValidationError("kind is only room")
        return value

    def validate_check_in_at(self, value):
        now = timezone.localdate()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value

    def validate_check_out_at(self, value):
        now = timezone.localdate()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value

    def validate(self, data):
        if data["check_out_at"] <= data["check_in_at"]:
            raise serializers.ValidationError("Check in should be smaller than check out.")

        is_exists = Booking \
                        .objects \
                        .filter(
                            check_in_at__lt=data["check_out_at"],
                            check_out_at__gt=data["check_in_at"],
                        ) \
                        .exists()
        if is_exists:
            raise serializers.ValidationError("Those (or some) of those dates are already taken.")

        return data

    def create(self, validated_data):
        return Booking.objects.create(**validated_data)
