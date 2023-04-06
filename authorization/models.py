import jwt
from django.db import models
from common.models import CommonModel
from django.conf import settings
from datetime import datetime, timedelta
from rest_framework.exceptions import AuthenticationFailed


class Token(CommonModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
    access_token = models.TextField()
    refresh_token = models.TextField()
    access_token_created_at = models.DateTimeField()
    access_token_expires_at = models.DateTimeField()
    refresh_token_created_at = models.DateTimeField()
    refresh_token_expires_at = models.DateTimeField()

    class Meta:
        db_table = "tokens"

    def __str__(self):
        return f"<Token id: {self.id}, user_id: {self.user_id}>"

    @classmethod
    def gen_jwt_token(cls, payload, token_type):
        if token_type == "access":
            exp = datetime.utcnow() + timedelta(days=1)
        elif token_type == "refresh":
            exp = datetime.utcnow() + timedelta(days=14)
        else:
            raise ValueError("Invalid Token Type.")

        payload['exp'] = exp
        payload['iat'] = datetime.utcnow()
        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    @classmethod
    def decoded_jwt_token(cls, token):
        try:
            return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError as err:
            raise AuthenticationFailed(err)
        except jwt.InvalidTokenError as err:
            raise AuthenticationFailed(err)
