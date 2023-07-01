from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_422_UNPROCESSABLE_ENTITY
from rooms.models import Amenity
from rooms.serializers import AmenityResponseSerializer, AmenityCreationSerializer, AmenityUpdateSerializer


class Amenities(APIView):
    def get(self, request):
        amenities = Amenity.objects.all()

        return Response(
            {
                "total": amenities.count(),
                "records": AmenityResponseSerializer(amenities, many=True).data,
            }
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


def see_one_room(request, id_):
    return HttpResponse(f"see one room. {id_}")


def see_one_order(request, name):
    return HttpResponse(f"{name}")
