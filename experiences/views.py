from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from . import models, serializers
from users.models import User
from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer, CreateExperienceBookingSerializer

from common.base_helper import BaseHelper


class ExperienceList(APIView, BaseHelper):
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        queryset = models.Experience \
            .objects \
            .all() \
            .order_by("-created_at")

        total = queryset.count()
        records = queryset.prefetch_related("perks", "category", "host")[self.offset(request):self.limit(request)]

        return Response(
            {
                "total": total,
                "records": serializers.ExperienceSerializer(records, many=True).data,
            }
        )

    def post(self, request):
        serializer = serializers.ExperienceDetailSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    experience = serializer.save(
                        host=User.objects.get(pk=1),
                    )
                    experience.add_perks(request.data.get("perk_ids", []))
            except Exception as e:
                raise exceptions.ParseError(e)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )


class ExperienceDetail(APIView):

    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return models.Experience.objects.get(pk=pk)
        except models.Experience.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        serializer = serializers.ExperienceDetailSerializer(experience)
        return Response(serializer.data)

    def put(self, request, pk):
        experience = self.get_object(pk)
        serializer = serializers.ExperienceDetailSerializer(
            experience,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    experience = serializer.save()
                    experience.add_perks(request.data.get("perk_ids", []))
            except Exception as e:
                raise exceptions.ParseError(e)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        else:
            raise exceptions.ParseError(serializer.errors)

    def delete(self, request, pk):
        experience = self.get_object(pk)
        if experience.host != request.user:
            raise exceptions.PermissionDenied
        experience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExperiencePerks(APIView, BaseHelper):

    def get(self, request, pk):
        queryset = models.Perk.objects.filter(experiences=pk)

        total = queryset.count()
        records = queryset[self.offset(request):self.limit(request)]

        return Response(
            {
                "total": total,
                "records": serializers.PerkSerializer(records, many=True).data,
            }
        )


class ExperienceBookings(APIView, BaseHelper):

    def get_object(self, pk):
        try:
            return models.Experience.objects.get(pk=pk)
        except models.Experience.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk):
        queryset = Booking \
            .objects \
            .filter(
                room=pk,
                kind=Booking.BookingKindChoices.EXPERIENCE,
                experience_time__gt=timezone.localtime().date(),
            ) \
            .order_by("-created_at")

        total = queryset.count()
        records = queryset.prefetch_related("experience", "user")[self.offset(request):self.limit(request)]

        return Response(
            {
                "total": total,
                "records": PublicBookingSerializer(records, many=True).data,
            }
        )

    def post(self, request, pk):
        serializer = CreateExperienceBookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                experience=pk,
                user=request.user,
                kind=Booking.BookingKindChoices.EXPERIENCE,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ExperienceBookingDetail(APIView):

    def get_booking(self, pk):
        try:
            return Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk, booking_pk):
        booking = self.get_booking(booking_pk)
        serializer = PublicBookingSerializer(booking)
        return Response(serializer.data)

    def put(self, request, pk, booking_pk):
        booking = self.get_booking(booking_pk)

        if booking.user != request.user:
            raise exceptions.PermissionDenied

        serializer = CreateExperienceBookingSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request, pk, booking_pk):
        booking = self.get_booking(booking_pk)

        if booking.user != request.user:
            raise exceptions.PermissionDenied

        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Perks(APIView):

    def get(self, request):
        perks = models.Perk.objects.all()
        serializer = serializers.PerkSerializer(perks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.PerkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class PerkDetail(APIView):

    def get_object(self, pk):
        try:
            return models.Perk.objects.get(pk=pk)
        except models.Perk.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk):
        perk = self.get_object(pk)
        serializer = serializers.PerkSerializer(perk)
        return Response(serializer.data)

    def put(self, request, pk):
        perk = self.get_object(pk)
        serializer = serializers.PerkSerializer(perk, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
