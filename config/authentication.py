import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import User


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        header = request.headers.get("Authorization", "")
        if not header:
            return None
        jwt_token = header.replace("Bearer ", '')
        decoded = jwt.decode(
            jwt_token,
            settings.SECRET_KEY,
            algorithms=["HS256"],
        )
        pk = decoded.get("pk")
        if not pk:
            raise AuthenticationFailed("Invalid Token")
        try:
            user = User.objects.get(pk=pk)
            return user, None
        except User.DoesNotExist:
            raise AuthenticationFailed("User Not Found")
