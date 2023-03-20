import pytest
import json


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

        params['password'] = None
        res = self.client.post(f"{self.url_prefix}/sign_up/", params)
        data = json.loads(res.content)
        assert res.status_code == 422
        assert data['password'][0] == "이 필드는 null일 수 없습니다."

        params['email'] = None
        params['password'] = "q1w2e3r4"
        res = self.client.post(f"{self.url_prefix}/sign_up/", params)
        data = json.loads(res.content)
        assert res.status_code == 422
        assert data['email'][0] == "이 필드는 null일 수 없습니다."

        params['email'] = "juren52@naver.com"
        res = self.client.post(f"{self.url_prefix}/sign_up/", params)
        data = json.loads(res.content)
        assert res.status_code != 422


