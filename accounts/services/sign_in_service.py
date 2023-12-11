from django.contrib.auth import login, authenticate
from django.core.exceptions import ObjectDoesNotExist

from users.models import User


class SignInService:
    def __init__(self, request, data):
        self.request = request
        self.email = data['email']
        self.password = data['password']

    def execute(self) -> User:
        user = authenticate(
            self.request,
            email=self.email,
            password=self.password,
        )

        if user is None:
            raise ObjectDoesNotExist

        login(self.request, user)
        return user