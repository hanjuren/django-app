from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import PrivateUserSerializer, UserUpdateSerializer, UserAvatarUpdateSerializer
from users.services.user_service import UserService


class UserDetail(APIView):
    permission_classes = [IsAuthenticated]
    _user_service = UserService()

    def get(self, request, pk):
        user = self._user_service.get_user(pk)
        return Response(PrivateUserSerializer(user).data)

    def put(self, request, pk):
        serializer = UserUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self._user_service.update_user(pk, serializer.validated_data)

        return Response(PrivateUserSerializer(user).data)


class Avatar(APIView):
    permission_classes = [IsAuthenticated]
    _user_service = UserService()

    @swagger_auto_schema(
        responses={200: PrivateUserSerializer()},
        tags=["users"]
    )
    def patch(self, request, pk):
        serializer = UserAvatarUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self._user_service.update_avatar(pk, serializer.validated_data)

        return Response(PrivateUserSerializer(user).data)
