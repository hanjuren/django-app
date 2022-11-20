from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Photo


class PhotoDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise exceptions.NotFound

    def delete(self, request, pk):
        current_user = request.user
        photo = self.get_object(pk)

        if (photo.room and photo.room.owner != current_user) or (photo.experience and photo.experience.host != current_user):
            raise exceptions.PermissionDenied
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
