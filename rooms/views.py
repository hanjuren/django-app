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


class AmenityDetail(APIView):
    def get(self, request, id_):
        amenity = Amenity.objects.get(id=id_)
        return Response(AmenityResponseSerializer(amenity).data)

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
