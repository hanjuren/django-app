import pytest
import json

pytestmark = pytest.mark.django_db


class TestRoomApi:
    @pytest.fixture(autouse=True)
    def set_up(self, client):
        self.url_prefix = "/api/v1/rooms/"
        self.client = client

    def test_rooms(self, user_factory, room_factory):
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
