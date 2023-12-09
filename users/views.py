from django.contrib.auth import login, logout, authenticate
from django.core.exceptions import BadRequest
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from users.serializers import PrivateUserSerializer
from users.services.user_service import UserService

class Users(APIView):
    _user_service = UserService()

    swagger_auto_schema(
        responses={201: PrivateUserSerializer()},
        tags=["users"]
    )
    def post(self, request):
        user = self._user_service.create_user(request)

        return Response(
            PrivateUserSerializer(user).data,
            status=HTTP_201_CREATED
        )


class UserDetail(APIView):
    permission_classes = [IsAuthenticated]
    _user_service = UserService()

    def get(self, request, pk):
        user = self._user_service.get_user(pk)

        return Response(PrivateUserSerializer(user).data)

    def put(self, request, pk):
        user = self._user_service.get_user(pk)
        self._user_service.update_user(user, request.data)

        return Response(PrivateUserSerializer(user).data)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]
    _user_service = UserService()

    swagger_auto_schema(
        responses={200: PrivateUserSerializer()},
        tags=["users"]
    )
    def put(self, request, pk):
        user = self._user_service.get_user(pk)
        if user.id != request.user.id:
            raise PermissionDenied

        self._user_service.change_password(user, request.data)

        return Response(PrivateUserSerializer(user).data)


class SignIn(APIView):
    _user_service = UserService()

    def post(self, request):
        try:
            user = self._user_service.sign_in(request)
            return Response(
                PrivateUserSerializer(user).data,
                status=HTTP_201_CREATED
            )
        except BadRequest as e:
            return Response(
                {"message": e.args[0]},
                status=HTTP_400_BAD_REQUEST
            )


class SignOut(APIView):
    permission_classes = [IsAuthenticated]
    _user_service = UserService()

    def post(self, request):
        self._user_service.sign_out(request)
        return Response({"message": "success"})


class Avatar(APIView):
    permission_classes = [IsAuthenticated]
    _user_service = UserService()

    @swagger_auto_schema(
        responses={200: PrivateUserSerializer()},
        tags=["users"]
    )
    def patch(self, request, pk):
        user = self._user_service.get_user(pk)
        self._user_service.update_avatar(user, request.data)

        return Response(PrivateUserSerializer(user).data)
