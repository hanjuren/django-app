import re

import jwt
import pytest
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from authorization import tokens
from datetime import datetime, timedelta, timezone

pytestmark = pytest.mark.django_db


def test_gen_jwt_token_invalid_token_type():
    payload = {}
    token_type = "invalid"
    with pytest.raises(ValueError) as err:
        tokens.gen_jwt_token(payload, token_type)
    assert str(err.value) == "Invalid Token Type."


def test_gen_jwt_token_access_token():
    payload = {"id": 1, "email": "juren52@naver.com"}
    token_type = "access"
    access_token = tokens.gen_jwt_token(payload, token_type)
    decoded_token = tokens.decoded_jwt_token(access_token)

    assert decoded_token['id'] == 1
    assert decoded_token['email'] == "juren52@naver.com"

    access_exp = datetime.fromtimestamp(decoded_token["exp"], tz=timezone.utc)
    access_exp_approx = (datetime.utcnow() + timedelta(days=1)).replace(microsecond=0, tzinfo=timezone.utc)
    assert access_exp > datetime.utcnow().replace(tzinfo=timezone.utc)
    assert access_exp == pytest.approx(access_exp_approx, abs=1)

    access_iat = datetime.fromtimestamp(decoded_token["iat"], tz=timezone.utc)
    access_iat_approx = datetime.utcnow().replace(microsecond=0, tzinfo=timezone.utc)
    assert access_iat == pytest.approx(access_iat_approx, abs=1)


def test_gen_jwt_token_refresh_token():
    payload = {"id": 1, "email": "juren52@naver.com"}
    token_type = "refresh"
    refresh_token = tokens.gen_jwt_token(payload, token_type)
    decoded_token = tokens.decoded_jwt_token(refresh_token)

    assert decoded_token['id'] == 1
    assert decoded_token['email'] == "juren52@naver.com"

    refresh_exp = datetime.fromtimestamp(decoded_token['exp'], tz=timezone.utc)
    refresh_exp_approx = (datetime.utcnow() + timedelta(days=14)).replace(microsecond=0, tzinfo=timezone.utc)
    assert refresh_exp > datetime.utcnow().replace(tzinfo=timezone.utc)
    assert refresh_exp == pytest.approx(refresh_exp_approx, abs=1)

    refresh_iat = datetime.fromtimestamp(decoded_token["iat"], tz=timezone.utc)
    refresh_iat_approx = datetime.utcnow().replace(microsecond=0, tzinfo=timezone.utc)
    assert refresh_iat == pytest.approx(refresh_iat_approx, abs=1)


def test_decoded_jwt_token_with_error():
    payload = {
        "id": 1,
        "email": "juren52@naver.com",
        "exp": datetime.utcnow() - timedelta(minutes=1)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    with pytest.raises(AuthenticationFailed, match=re.escape("Signature has expired")):
        tokens.decoded_jwt_token(token)

    token = jwt.encode({'some': 'payload'}, settings.SECRET_KEY, algorithm='HS256')
    with pytest.raises(AuthenticationFailed, match=re.escape("Signature verification failed")):
        tokens.decoded_jwt_token(token[:-3] + 'xyz')
