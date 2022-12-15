from django.utils import timezone
from rest_framework import serializers
from .models import Booking


class CreateRoomBookingSerializer(serializers.ModelSerializer):

    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests",
        )

    def validate_check_in(self, value):
        now = timezone.localtime().date()
        if value < now:
            raise serializers.ValidationError("Can't book in the past.")
        return value

    def validate_check_out(self, value):
        now = timezone.localtime().date()
        if value < now:
            raise serializers.ValidationError("Can't book in the past.")
        return value

    def validate(self, attrs):
        if attrs['check_out'] <= attrs['check_in']:
            raise serializers.ValidationError("Check In should be smaller then Check Out.")
        if Booking.objects.filter(
            check_in__lt=attrs['check_out'],
            check_out__gt=attrs['check_in'],
        ).exists():
            raise serializers.ValidationError("Those (or some) of those dates are already taken.")
        return attrs


class CreateExperienceBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = (
            "experience_time",
            "guests",
        )

    def validate_experience_time(self, value):
        now = timezone.localtime().data()
        if value < now:
            raise serializers.ValidationError("Cat't book in the past.")
        return value


class PublicBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
        )
