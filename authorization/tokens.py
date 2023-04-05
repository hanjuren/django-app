import jwt
from django.conf import settings
from datetime import datetime, timedelta


def gen_jwt_token(payload, token_type):
    if token_type == "access":
        exp = datetime.utcnow() + timedelta(days=1)
    elif token_type == "refresh":
        exp = datetime.utcnow() + timedelta(days=14)
    else:
        raise ValueError("Invalid Token Type.")

    payload['exp'] = exp
    payload['iat'] = datetime.utcnow()
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def decoded_jwt_token(token):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])