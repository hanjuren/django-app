from django.conf import settings
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Amenity, Room
from categories.models import Category
from .serializers import AmenitySerializer, RoomListSerializer, RoomDeatilSerializer
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer


class Rooms(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomListSerializer(
            rooms,
            many=True,
            context={"request": request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = RoomDeatilSerializer(data=request.data)
        if serializer.is_valid():
            # category
            category_pk = request.data.get("category_id")
            if not category_pk:
                raise exceptions.ParseError("Category is required.")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                    raise exceptions.ParseError("Category kind should be Rooms")
            except Category.DoesNotExist:
                raise exceptions.NotFound("Category Not Found")

            try:
                with transaction.atomic():
                    room = serializer.save(
                        owner=request.user,
                        category=category,
                    )
                    # amenities
                    for pk in request.data.get("amenity_ids", []):
                        amenity = Amenity.objects.get(pk=pk)
                        room.amenities.add(amenity)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception:
                raise exceptions.ParseError("Create Room Fail")
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class RoomDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDeatilSerializer(
            room,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_object(pk)

        if room.owner != request.user:
            raise exceptions.PermissionDenied

        serializer = RoomDeatilSerializer(room, data=request.data, partial=True)

        if serializer.is_valid():
            category_pk = request.data.get("category_id")
            if not category_pk:
                raise exceptions.ParseError("Category is required")

            try:
                category = Category.objects.get(pk=request.data.get("category_id"))
                if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                    raise exceptions.ParseError("Category kind should be rooms")
            except Category.DoesNotExist:
                raise exceptions.NotFound("Category is not found")

            try:
                with transaction.atomic():
                    room = serializer.save(category=category)

                    amenity_ids = request.data.get("amenity_ids", [])
                    if amenity_ids:
                        room.amenities.clear()
                        for amenity_pk in amenity_ids:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            room.amenities.add(amenity)

                    return Response(serializer.data)
            except Exception:
                raise exceptions.ParseError("Amenity is not found")
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request, pk):
        room = self.get_object(pk)
        if room.owner != request.user:
            raise exceptions.PermissionDenied
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoomReviews(APIView):

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk):
        try:
            page = int(request.query_params.get("page", 1))
        except ValueError:
            page = 1

        page_size = settings.PAGE_SIZE
        offset = (page - 1) * page_size
        limit = offset + page_size

        room = self.get_object(pk)
        serializer = ReviewSerializer(
            room.reviews.all()[offset:limit],
            many=True
        )
        return Response(serializer.data)


class RoomAmenities(APIView):

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk):
        try:
            page = int(request.query_params.get("page", 1))
        except ValueError:
            page = 1

        page_size = settings.PAGE_SIZE
        offset = (page - 1) * page_size
        limit = offset + page_size

        room = self.get_object(pk)
        serializer = AmenitySerializer(
            room.amenities.all()[offset:limit],
            many=True,
        )
        return Response(serializer.data)


class RoomPhotos(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise exceptions.NotFound

    def post(self, request, pk):
        room = self.get_object(pk)
        if request.user != room.owner:
            raise exceptions.PermissionDenied

        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(room=room)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class Amenities(APIView):

    def get(self, request):
        amenities = Amenity.objects.all()
        serializer = AmenitySerializer(amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class AmenityDetail(APIView):

    def get_amenity(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk):
        amenity = self.get_amenity(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, pk):
        amenity = self.get_amenity(pk)
        serializer = AmenitySerializer(amenity, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request, pk):
        amenity = self.get_amenity(pk)
        amenity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
