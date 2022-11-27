from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from . import models, serializers
from users.models import User
from common.base_helper import BaseHelper


class ExperienceList(APIView, BaseHelper):
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        print(request.headers)
        queryset = models.Experience \
            .objects \
            .all() \
            .order_by("-created_at")

        total = queryset.count()
        records = queryset \
            .prefetch_related("perks") \
            .select_related("category")[self.offset(request):self.limit(request)]

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
