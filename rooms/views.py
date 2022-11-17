from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions

from .models import Amenity, Room
from categories.models import Category
from .serializers import AmenitySerializer, RoomListSerializer, RoomDeatilSerializer


class Rooms(APIView):

    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomListSerializer(rooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        print(request.user.is_authenticated)
        print(request.user)
        if request.user.is_authenticated:
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

                room = serializer.save(
                    owner=request.user,
                    category=category,
                )

                # amenities
                for pk in request.data.get("amenity_ids", []):
                    try:
                        amenity = Amenity.objects.get(pk=pk)
                        room.amenities.add(amenity)
                    except Amenity.DoesNotExist:
                        pass

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            raise exceptions.NotAuthenticated


class RoomDetail(APIView):

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDeatilSerializer(room)
        return Response(serializer.data)

    def post(self, request, pk):
        pass


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
