from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_yasg.utils import swagger_auto_schema
from rooms.models import Room, Amenity
from rooms.serializers import AmenityResponseSerializer, AmenityListResponseSerializer, AmenityCreationSerializer, \
    AmenityUpdateSerializer, RoomsResponseSerializer, RoomListResponseSerializer, RoomResponseSerializer, \
    RoomCreationSerializer, RoomUpdateSerializer


class Rooms(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # GET /api/v1/rooms
    @swagger_auto_schema(responses={200: RoomListResponseSerializer()})
    def get(self, request):
        rooms = Room.objects.all()
        return Response(
            {
                "total": rooms.count(),
                "records": RoomsResponseSerializer(rooms, many=True).data,
            }
        )

    # POST /api/v1/rooms
    @swagger_auto_schema(
        request_body=RoomCreationSerializer,
        responses={200: RoomResponseSerializer()},
    )
    def post(self, request):
        serializer = RoomCreationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        room = serializer.save(user=request.user)
        room.add_amenities(request.data.get("amenity_ids", []))

        return Response(
            RoomResponseSerializer(room).data,
            status=HTTP_201_CREATED,
        )


class RoomDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # GET /api/v1/rooms/1
    @swagger_auto_schema(responses={200: RoomResponseSerializer()})
    def get(self, request, id_):
        room = Room.objects.get(id=id_)
        return Response(RoomResponseSerializer(room).data)

    # PUT /api/v1/rooms/1
    @swagger_auto_schema(responses={200: RoomResponseSerializer()})
    def put(self, request, id_):
        room = Room.objects.get(id=id_)
        if room.user != request.user:
            raise PermissionDenied

        serializer = RoomUpdateSerializer(room, data=request.data)
        serializer.is_valid(raise_exception=True)

        room = serializer.save()
        room.add_amenities(request.data.get("amenity_ids", []))

        return Response(RoomResponseSerializer(room).data)

    # DELETE /api/v1/rooms/1
    def delete(self, request, id_):
        room = Room.objects.get(id=id_)
        if room.user != request.user:
            raise PermissionDenied

        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Amenities(APIView):
    @swagger_auto_schema(responses={200: AmenityListResponseSerializer()})
    def get(self, request):
        amenities = Amenity.objects.all()

        return Response(
            {
                "total": amenities.count(),
                "records": AmenityResponseSerializer(amenities, many=True).data,
            }
        )

    @swagger_auto_schema(
        request_body=AmenityCreationSerializer,
        responses={201: AmenityResponseSerializer()}
    )
    def post(self, request):
        serializer = AmenityCreationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=HTTP_422_UNPROCESSABLE_ENTITY,
            )
        else:
            amenity = serializer.save()

            return Response(
                AmenityResponseSerializer(amenity).data,
                status=HTTP_201_CREATED,
            )


class AmenityDetail(APIView):
    @swagger_auto_schema(responses={200: AmenityResponseSerializer()})
    def get(self, request, id_):
        amenity = Amenity.objects.get(id=id_)
        return Response(AmenityResponseSerializer(amenity).data)

    @swagger_auto_schema(
        request_body=AmenityUpdateSerializer,
        responses={200: AmenityResponseSerializer()}
    )
    def put(self, request, id_):
        amenity = Amenity.objects.get(id=id_)
        serializer = AmenityUpdateSerializer(
            amenity,
            data=request.data,
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=HTTP_422_UNPROCESSABLE_ENTITY,
            )
        else:
            serializer.save()
            return Response(AmenityResponseSerializer(amenity).data)

    def delete(self, request, id_):
        amenity = Amenity.objects.get(id=id_)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)
