from django.contrib.auth import login, logout, authenticate
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from users.models import User
from users.serializers import PrivateUserSerializer, UserCreationSerializer, \
    UserUpdateSerializer, UserAvatarUpdateSerializer, UserChangePasswordSerializer

class Users(APIView):
    swagger_auto_schema(
        responses={201: PrivateUserSerializer()},
        tags=["users"]
    )
    def post(self, request):
        serializer = UserCreationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            PrivateUserSerializer(user).data,
            status=HTTP_201_CREATED
        )


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    swagger_auto_schema(
        responses={200: PrivateUserSerializer()},
        tags=["users"]
    )
    def put(self, request, pk):
        user = User.objects.get(id=pk)
        if user.id != request.user.id:
            raise PermissionDenied

        serializer = UserChangePasswordSerializer(
            user,
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(PrivateUserSerializer(user).data)


class SignIn(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(
            request,
            email=email,
            password=password,
        )
        if user is None:
            return Response(
                {"message": "Wrong Password"},
                status=HTTP_400_BAD_REQUEST
            )

        login(request, user)
        return Response({"message": "success"})


class SignOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "success"})


class Me(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: PrivateUserSerializer()},
        tags=["me"]
    )
    def get(self, request):
        user = request.user
        return Response(PrivateUserSerializer(user).data)

    @swagger_auto_schema(
        responses={200: PrivateUserSerializer()},
        tags=["me"]
    )
    def put(self, request):
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(PrivateUserSerializer(user).data)


class Avatar(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: PrivateUserSerializer()},
        tags=["users/avatar"]
    )
    def put(self, request):
        user = request.user
        serializer = UserAvatarUpdateSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(PrivateUserSerializer(user).data)

    @swagger_auto_schema(
        tags=["users/avatar"]
    )
    def delete(self, request):
        user = request.user
        user.delete_avatar()
        user.avatar = None
        user.save()

        return Response(PrivateUserSerializer(user).data)
