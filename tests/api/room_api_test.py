import pytest
import json

pytestmark = pytest.mark.django_db


class TestRoomApi:
    @pytest.fixture(autouse=True)
    def set_up(self, client):
        self.url_prefix = "/api/v1/rooms/"
        self.client = client

    def test_get_rooms(self, user_factory, room_factory):
        user = user_factory.create()
        room_factory.create_batch(5, owner=user)

        response = self.client.get(self.url_prefix)
        data = response.get('json_response')

        assert response.get('status_code') == 200
        assert isinstance(data, list)
        assert len(data) == 5

        expected_keys = ['pk', 'name', 'country', 'city', 'price', 'rating', 'is_owner', 'photos']
        got_keys = list(data[0].keys())
        assert all(k in expected_keys for k in got_keys)

    def test_post_room_with_validation_error(self, user_factory):
        user = user_factory.create()
        token = user.gen_jwt_token()

        params = {
            "name": "test rooms",
            "country": "a",
            "city": "의왕시",
            "price": 12000,
            "rooms": 2,
            "toilets": 1,
            "description": "test rooms description",
            "address": "경기도 의왕시 포일세거리로 23",
            "pet_friendly": False,
            "kind": "entire_place"
        }
        res = self.client.post(
            self.url_prefix,
            params,
            token,
        )
        data = json.loads(res.content)
        print(data)
        assert res.status_code == 422
        assert data['amenities'][0] == '이 필드는 필수 항목입니다.'
