from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.conf import settings
from .models import Photo


class PhotoDetail(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id_):
        photo = Photo.objects.get(id=id_)

        if (photo.room and photo.room.user != request.user) or (
                photo.experience and photo.experience.user != request.user
        ):
            raise PermissionDenied
        photo.delete()

        return Response(status=HTTP_204_NO_CONTENT)


