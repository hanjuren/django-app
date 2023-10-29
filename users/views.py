from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from users.serializers import PrivateUserSerializer, UserUpdateSerializer, UserAvatarUpdateSerializer

class Me(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: PrivateUserSerializer()},
        tags=["me"]
    )
    def get(self, request):
        user = request.user
        return Response(PrivateUserSerializer(user).data)

    def put(self, request):
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(PrivateUserSerializer(user).data)


class Avatar(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = UserAvatarUpdateSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(PrivateUserSerializer(user).data)

    def delete(self, request):
        user = request.user
        user.delete_avatar()
        user.avatar = None
        user.save()

        return Response(PrivateUserSerializer(user).data)
