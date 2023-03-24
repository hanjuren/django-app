import pytest
import json

pytestmark = pytest.mark.django_db


class TestUserApi:
    """
    유저 api
    """
    @pytest.fixture(autouse=True)
    def set_up(self, client):
        self.url_prefix = "/api/v1/users"
        self.client = client

    def test_me_is_authenticated(self):
        res = self.client.get(f"{self.url_prefix}/me/")
        print(res)
        assert res.status_code == 403

    def test_me(self, user_factory):
        user = user_factory.create()

        res = self.client.get(
            f"{self.url_prefix}/me/",
            token=user.gen_jwt_token(),
        )
        data = json.loads(res.content)
        print(json.dumps(data, indent=2))
