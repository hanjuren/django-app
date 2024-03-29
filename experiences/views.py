from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_422_UNPROCESSABLE_ENTITY
from drf_yasg.utils import swagger_auto_schema
from config.pagination import Pagination
from experiences.models import Perk
from experiences.serializers import PerkResponseSerializer, PerkListSerializer, \
    PerkCreationSerializer, PerkUpdateSerializer


class Perks(APIView, Pagination):
    @swagger_auto_schema(
        responses={200: PerkListSerializer()},
        tags=["experiences/perks"]
    )
    def get(self, request):
        query = Perk.objects.all()

        total = query.count()
        offset = self.offset(request)
        limit = self.limit(request) + offset
        records = query.order_by('created_at')[offset:limit]

        return Response(
            {
                "total": total,
                "records": PerkResponseSerializer(records, many=True).data,
            }
        )

    @swagger_auto_schema(
        request_body=PerkCreationSerializer,
        responses={201: PerkResponseSerializer()},
        tags=["experiences/perks"]
    )
    def post(self, request):
        serializer = PerkCreationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=HTTP_422_UNPROCESSABLE_ENTITY,
            )
        else:
            perk = serializer.save()

            return Response(
                PerkResponseSerializer(perk).data,
                status=HTTP_201_CREATED
            )


class PerkDetail(APIView):
    @swagger_auto_schema(
        responses={200: PerkResponseSerializer()},
        tags=["experiences/perks"]
    )
    def get(self, request, id_):
        perk = Perk.objects.get(id=id_)
        return Response(PerkResponseSerializer(perk).data)

    @swagger_auto_schema(
        request_body=PerkUpdateSerializer,
        responses={200: PerkResponseSerializer()},
        tags=["experiences/perks"]
    )
    def put(self, request, id_):
        perk = Perk.objects.get(id=id_)
        serializer = PerkUpdateSerializer(
            perk,
            data=request.data,
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            serializer.save()
            return Response(PerkResponseSerializer(perk).data)

    @swagger_auto_schema(tags=["experiences/perks"])
    def delete(self, request, id_):
        perk = Perk.objects.get(id=id_)
        perk.delete()
        return Response(status=HTTP_204_NO_CONTENT)
