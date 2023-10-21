from django.utils import timezone
from rest_framework import serializers, exceptions
from bookings.models import Booking


class RoomBookingCreationSerializer(serializers.Serializer):
    kind = serializers.ChoiceField(choices=Booking.BookingKindChoices)
    check_in_at = serializers.DateField()
    check_out_at = serializers.DateField()
    guests = serializers.IntegerField(min_value=1)

    def validate(self, data):
        check_in_at = data.get("check_in_at")
        check_out_at = data.get("check_out_at")

        if check_in_at < timezone.localdate():
            raise exceptions.ParseError("체크인 정보를 확인 하세요.")

        if check_in_at >= check_out_at:
            raise exceptions.ParseError("체크아웃 정보를 확인 하세요.")

        return data

    def create(self, validated_data):
        return Booking.objects.create(**validated_data)
