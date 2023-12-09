from django.contrib.auth import login, logout, authenticate
from django.core.exceptions import BadRequest
from users.models import User
from users.repositories.user_repository import UserRepository
from users.serializers import UserCreationSerializer, UserUpdateSerializer, UserChangePasswordSerializer, \
    UserAvatarUpdateSerializer


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def create_user(self, request) -> User:
        serializer = UserCreationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.repository.create(serializer.validated_data)

        return user

    def get_user(self, pk) -> User:
        return self.repository.get(pk)

    def update_user(self, user, data) -> User:
        serializer = UserUpdateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.repository.update(user, serializer.validated_data)

        return user

    def change_password(self, user, data) -> User:
        serializer = UserChangePasswordSerializer(
            data=data,
            context={"user": user}
        )
        serializer.is_valid(raise_exception=True)
        self.repository.set_password(
            user,
            serializer.validated_data['new_password'],
        )

        return user

    def sign_in(self, request) -> User | None:
        user = authenticate(
            request,
            email=request.data['email'],
            password=request.data['password']
        )
        if user:
            login(request, user)
            return user
        else:
            raise BadRequest("fail")

    def sign_out(self, request) -> None:
        logout(request)

    def update_avatar(self, user, data) -> User:
        serializer = UserAvatarUpdateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.repository.update_avatar(user, serializer.validated_data)

        return user


