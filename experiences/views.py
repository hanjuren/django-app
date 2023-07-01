from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_422_UNPROCESSABLE_ENTITY
from experiences.models import Perk
from experiences.serializers import PerkResponseSerializer, PerkCreationSerializer


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
