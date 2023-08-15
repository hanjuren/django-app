import jwt
from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import User


class JwtAuthentication(TokenAuthentication):
    def authenticate(self, request):
        header = request.headers.get("Authorization")
        if not header:
            return None

        token = header.replace("Bearer ", "")
        try:
            decoded = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=["HS256"],
            )
            user_id = decoded.get('user_id')
            user = User.objects.get(id=user_id)

            return user, None
        except Exception as e:
            raise AuthenticationFailed(e)
