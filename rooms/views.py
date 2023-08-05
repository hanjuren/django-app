from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_422_UNPROCESSABLE_ENTITY
from drf_yasg.utils import swagger_auto_schema
from rooms.models import Amenity
from rooms.serializers import AmenityResponseSerializer, AmenityListResponseSerializer, \
    AmenityCreationSerializer, AmenityUpdateSerializer


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
