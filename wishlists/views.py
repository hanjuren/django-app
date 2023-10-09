from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from config.pagination import Pagination

from wishlists.serializers import *
from wishlists.models import *


class Wishlists(APIView, Pagination):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: WishlistListResponseSerializer()},
        tags=["wishlists"]
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

    def post(self, request):
        pass
