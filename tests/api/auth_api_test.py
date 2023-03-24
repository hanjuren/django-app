import pytest
import json
import re
from users.models import User

pytestmark = pytest.mark.django_db


class TestSignUp:
    """
    유저 생성 테스트
    """
    @pytest.fixture(autouse=True)
    def set_up(self, client):
        self.url_prefix = "/api/v1/auth"
        self.client = client

    def test_serializer_errors(self):
        params = {"email": "juren52@naver.com"}
        res = self.client.post(f"{self.url_prefix}/sign_up/", params)
        data = json.loads(res.content)

        assert res.status_code == 422
        assert data['password'][0] == "이 필드는 필수 항목입니다."

        params.update({"password": None})
        res = self.client.post(f"{self.url_prefix}/sign_up/", params)
        data = json.loads(res.content)

        assert res.status_code == 422
        assert data['password'][0] == "이 필드는 null일 수 없습니다."

        params.update({"email": None, "password": "qwer1234"})
        res = self.client.post(f"{self.url_prefix}/sign_up/", params)
        data = json.loads(res.content)

        assert res.status_code == 422
        assert data['email'][0] == "이 필드는 null일 수 없습니다."

        params.update({"email": "juren52@naver.com"})
        res = self.client.post(f"{self.url_prefix}/sign_up/", params)

        assert res.status_code != 422

    def test_save_user(self):
        params = {"email": "juren52@naver.com", "password": "q1w2e3r4"}

        res = self.client.post(f"{self.url_prefix}/sign_up/", params)
        data = json.loads(res.content)

        assert res.status_code == 201
        assert User.objects.count() == 1
        assert data['success'] is True


class TestSignIn:
    """
    로그인 테스트
    """
    @pytest.fixture(autouse=True)
    def set_up(self, client):
        self.url_prefix = "/api/v1/auth/sign_in/"
        self.client = client

    def test_email_is_required(self):
        params = {"email": "juren52@naver.com"}
        res = self.client.post(self.url_prefix, params)
        data = json.loads(res.content)

        assert res.status_code == 400
        assert re.match("잘못된 요청입니다.", data['error']['message'])

    def test_password_is_required(self):
        params = {"password": "q1w2e3r4"}
        res = self.client.post(self.url_prefix, params)
        data = json.loads(res.content)

        assert res.status_code == 400
        assert re.match("잘못된 요청입니다.", data['error']['message'])

    def test_not_found_user(self):
        params = {"email": "juren52@naver.com", "password": "q1w2e3r4"}
        res = self.client.post(self.url_prefix, params)
        data = json.loads(res.content)

        assert res.status_code == 404
        assert re.match("Not Found", data['error']['message'])

    def test_sign_in(self):
        sign_up_params = {"email": "juren52@naver.com", "password": "q1w2e3r4"}
        self.client.post("/api/v1/auth/sign_up/", sign_up_params)

        sign_in_params = sign_up_params.copy()
        res = self.client.post(self.url_prefix, sign_in_params)
        data = json.loads(res.content)

        assert res.status_code == 201
        assert data['success'] is True
        assert data['access_token'] is not None
