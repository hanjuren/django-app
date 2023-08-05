from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_422_UNPROCESSABLE_ENTITY
from experiences.models import Perk
from experiences.serializers import PerkResponseSerializer, PerkCreationSerializer, PerkUpdateSerializer


class Perks(APIView):
    def get(self, request):
        perks = Perk.objects.all()

        return Response(
            {
                "total": perks.count(),
                "records": PerkResponseSerializer(perks, many=True).data,
            }
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
    def get(self, request, id_):
        perk = Perk.objects.get(id=id_)
        return Response(PerkResponseSerializer(perk).data)

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

    def delete(self, request, id_):
        perk = Perk.objects.get(id=id_)
        perk.delete()
        return Response(status=HTTP_204_NO_CONTENT)
