from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.views import APIView

from bookings.serializers import PublicBookingsResponseSerializer, PublicBookingListResponseSerializer, \
    RoomBookingCreationSerializer, PublicRoomBookingResponseSerializer
from config.pagination import Pagination
from medias.serializers import PhotoCreationSerializer, PhotoResponseSerializer
from reviews.serializers import ReviewsResponseSerializer, ReviewListResponseSerializer, ReviewCreationSerializer
from rooms.models import Room, Amenity
from rooms.serializers import AmenityResponseSerializer, AmenityListResponseSerializer, AmenityCreationSerializer, \
    AmenityUpdateSerializer, RoomsResponseSerializer, RoomListResponseSerializer, RoomResponseSerializer, \
    RoomCreationSerializer, RoomUpdateSerializer


class Rooms(APIView, Pagination):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # GET /api/v1/rooms
    @swagger_auto_schema(
        responses={200: RoomListResponseSerializer()},
        tags=["rooms"]
    )
    def get(self, request):
        query = Room.objects.all()

        total = query.count()

        offset = self.offset(request)
        limit = self.limit(request) + offset
        records = query \
                    .prefetch_related("user", "photos", "reviews") \
                    .order_by('created_at')[offset:limit]

        return Response(
            {
                "total": total,
                "records": RoomsResponseSerializer(
                    records,
                    many=True,
                    context={"request": request},
                ).data,
            }
        )

    # POST /api/v1/rooms
    @swagger_auto_schema(
        request_body=RoomCreationSerializer,
        responses={200: RoomResponseSerializer()},
        tags=["rooms"]
    )
    def post(self, request):
        serializer = RoomCreationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        room = serializer.save(user=request.user)
        room.add_amenities(request.data.get("amenity_ids", []))

        return Response(
            RoomResponseSerializer(
                room,
                context={"request": request},
            ).data,
            status=HTTP_201_CREATED,
        )


class RoomDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # GET /api/v1/rooms/1
    @swagger_auto_schema(
        responses={200: RoomResponseSerializer()},
        tags=["rooms"]
    )
    def get(self, request, id_):
        room = Room.objects.get(id=id_)
        serializer = RoomResponseSerializer(room, context={"request": request})
        return Response(serializer.data)

    # PUT /api/v1/rooms/1
    @swagger_auto_schema(
        responses={200: RoomResponseSerializer()},
        tags=["rooms"]
    )
    def put(self, request, id_):
        room = Room.objects.get(id=id_)
        if room.user != request.user:
            raise PermissionDenied

        update_serializer = RoomUpdateSerializer(room, data=request.data)
        update_serializer.is_valid(raise_exception=True)

        room = update_serializer.save()
        room.add_amenities(request.data.get("amenity_ids", []))

        serializer = RoomResponseSerializer(room, context={"request": request})
        return Response(serializer.data)

    # DELETE /api/v1/rooms/1
    @swagger_auto_schema(tags=["rooms"])
    def delete(self, request, id_):
        room = Room.objects.get(id=id_)
        if room.user != request.user:
            raise PermissionDenied

        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RoomReviews(APIView, Pagination):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        responses={200: ReviewListResponseSerializer()},
        tags=["rooms/:id/reviews"]
    )
    def get(self, request, id_):
        room = Room.objects.get(id=id_)
        query = room.reviews.all()

        total = query.count()
        offset = self.offset(request)
        limit = self.limit(request) + offset
        records = query.order_by('created_at')[offset:limit]

        return Response(
            {
                "total": total,
                "records": ReviewsResponseSerializer(
                    records,
                    many=True,
                ).data,
            }
        )

    @swagger_auto_schema(
        request_body=ReviewCreationSerializer,
        responses={200: ReviewsResponseSerializer()},
        tags=["rooms/:id/reviews"]
    )
    def post(self, request, id_):
        room = Room.objects.get(id=id_)

        serializer = ReviewCreationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = serializer.save(
            user=request.user,
            room=room
        )

        return Response(ReviewsResponseSerializer(review).data, status=HTTP_201_CREATED)


class RoomPhotos(APIView):
    @swagger_auto_schema(
        request_body=PhotoCreationSerializer,
        responses={201: PhotoResponseSerializer()},
        tags=["rooms/:id/photos"]
    )
    def post(self, request, id_):
        room = Room.objects.get(id=id_)

        serializer = PhotoCreationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        photo = serializer.save(room=room)

        return Response(PhotoResponseSerializer(photo).data, status=HTTP_201_CREATED)


class RoomBookings(APIView, Pagination):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # GET /api/v1/rooms/1/bookings
    @swagger_auto_schema(
        responses={200: PublicBookingListResponseSerializer()},
        tags=["rooms/:id/bookings"]
    )
    def get(self, request, id_):
        room = Room.objects.get(id=id_)
        query = room \
                    .bookings \
                    .filter(check_in_at__gte=timezone.localtime())

        total = query.count()

        offset = self.offset(request)
        limit = self.limit(request) + offset
        records = query.order_by('-created_at')[offset:limit]

        return Response(
            {
                "total": total,
                "records": PublicBookingsResponseSerializer(
                    records,
                    many=True,
                ).data,
            }
        )

    def post(self, request, id_):
        room = Room.objects.get(id=id_)

        serializer = RoomBookingCreationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        booking = serializer.save(
            room=room,
            user=request.user,
        )

        return Response(
            PublicRoomBookingResponseSerializer(
                booking,
                context={"request": request}
            ).data,
            status=HTTP_201_CREATED,
        )


class Amenities(APIView, Pagination):
    @swagger_auto_schema(
        responses={200: AmenityListResponseSerializer()},
        tags=["rooms/amenities"]
    )
    def get(self, request):
        query = Amenity.objects.all()

        total = query.count()
        offset = self.offset(request)
        limit = self.limit(request) + offset
        records = query.order_by('created_at')[offset:limit]

        return Response(
            {
                "total": total,
                "records": AmenityResponseSerializer(records, many=True).data,
            }
        )

    @swagger_auto_schema(
        request_body=AmenityCreationSerializer,
        responses={201: AmenityResponseSerializer()},
        tags=["rooms/amenities"]
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
    @swagger_auto_schema(
        responses={200: AmenityResponseSerializer()},
        tags=["rooms/amenities"]
    )
    def get(self, request, id_):
        amenity = Amenity.objects.get(id=id_)
        return Response(AmenityResponseSerializer(amenity).data)

    @swagger_auto_schema(
        request_body=AmenityUpdateSerializer,
        responses={200: AmenityResponseSerializer()},
        tags=["rooms/amenities"]
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

    @swagger_auto_schema(tags=["rooms/amenities"])
    def delete(self, request, id_):
        amenity = Amenity.objects.get(id=id_)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)
