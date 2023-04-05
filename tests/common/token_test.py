import pytest
from authorization import tokens
from datetime import datetime, timedelta, timezone
import time

pytestmark = pytest.mark.django_db


def test_gen_jwt_token_invalid_token_type():
    payload = {}
    token_type = "invalid"
    with pytest.raises(ValueError) as err:
        tokens.gen_jwt_token(payload, token_type)
    assert str(err.value) == "Invalid Token Type."


def test_gen_jwt_token_access_token(user_factory):
    payload = {"id": 1, "email": "juern52@naver.com"}
    token_type = "access"
    access_token = tokens.gen_jwt_token(payload, token_type)
    decoded_token = tokens.decoded_jwt_token(access_token)

    assert decoded_token['id'] == 1
    assert decoded_token['email'] == "juern52@naver.com"

    access_exp = datetime.fromtimestamp(decoded_token["exp"], tz=timezone.utc)
    access_exp_approx = (datetime.utcnow() + timedelta(days=1)).replace(microsecond=0, tzinfo=timezone.utc)
    assert access_exp > datetime.utcnow().replace(tzinfo=timezone.utc)
    assert access_exp == pytest.approx(access_exp_approx, abs=1)

    access_iat = datetime.fromtimestamp(decoded_token["iat"], tz=timezone.utc)
    access_iat_approx = datetime.utcnow().replace(microsecond=0, tzinfo=timezone.utc)
    assert access_iat == pytest.approx(access_iat_approx, abs=1)
