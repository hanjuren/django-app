from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from config.pagination import Pagination

from wishlists.serializers import *
from wishlists.models import *
from rooms.models import Room


class Wishlists(APIView, Pagination):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: WishlistListResponseSerializer()},
        tags=["wishlists"],
    )
    def get(self, request):
        query = Wishlist.objects.filter(user=request.user)

        total = query.count()

        offset = self.offset(request)
        limit = self.limit(request) + offset
        records = query \
                    .prefetch_related(
                        "rooms",
                        "rooms__user",
                        "rooms__reviews",
                        "rooms__photos",
                    ) \
                    .order_by("created_at") \
                    [offset:limit]

        return Response(
            {
                "total": total,
                "records": WishlistsResponseSerializer(
                    records,
                    many=True,
                    context={"request": request},
                ).data
            }
        )

    @swagger_auto_schema(
        request_body=WishlistCreationSerializer,
        responses={201: WishlistsResponseSerializer()},
        tags=["wishlists"],
    )
    def post(self, request):
        serializer = WishlistCreationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        wishlist = serializer.save(user=request.user)

        # wishlist 생성시 rooms, experiences 가 없기 때문에 N+1 쿼리 발생 문제는 없음.
        return Response(
            WishlistsResponseSerializer(
                wishlist,
                context={"request": request},
            ).data,
            status=HTTP_201_CREATED
        )


class WishlistDetail(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: WishlistsResponseSerializer()},
        tags=["wishlists"],
    )
    def get(self, request, id_):
        wishlist = Wishlist \
                        .objects \
                        .prefetch_related(
                            "rooms",
                            "rooms__user",
                            "rooms__reviews",
                            "rooms__photos",
                        ) \
                        .get(id=id_, user=request.user)

        return Response(
            WishlistsResponseSerializer(
                wishlist,
                context={"request": request},
            ).data
        )

    @swagger_auto_schema(
        request_body=WishlistUpdateSerializer,
        responses={200: WishlistsResponseSerializer()},
        tags=["wishlists"],
    )
    def put(self, request, id_):
        wishlist = Wishlist \
                        .objects \
                        .prefetch_related(
                            "rooms",
                            "rooms__user",
                            "rooms__reviews",
                            "rooms__photos",
                        ) \
                        .get(id=id_, user=request.user)

        serializer = WishlistUpdateSerializer(wishlist, data=request.data)
        serializer.is_valid(raise_exception=True)
        wishlist = serializer.save()

        return Response(
            WishlistsResponseSerializer(
                wishlist,
                context={"request": request},
            ).data
        )

    @swagger_auto_schema(tags=["wishlists"])
    def delete(self, request, id_):
        wishlist = Wishlist.objects.get(id=id_, user=request.user)
        wishlist.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class WishlistRooms(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: WishlistsResponseSerializer()},
        tags=["wishlists/:id/rooms/:room_id"],
    )
    def put(self, request, id_, room_id):
        wishlist = Wishlist.objects.get(id=id_, user=request.user)
        room = Room.objects.get(id=room_id)

        if wishlist.rooms.filter(id=room.id).exists():
            wishlist.rooms.remove(room)
        else:
            wishlist.rooms.add(room)

        wishlist = Wishlist \
                        .objects \
                        .prefetch_related(
                            "rooms",
                            "rooms__user",
                            "rooms__reviews",
                            "rooms__photos",
                        ) \
                        .get(id=wishlist.id)

        return Response(
            WishlistsResponseSerializer(
                wishlist,
                context={"request": request},
            ).data
        )
