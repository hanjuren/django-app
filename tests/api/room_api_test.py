import pytest
import json
from tests.factories import *
from tests.conftest import *

pytestmark = pytest.mark.django_db


class TestRoomApi:
    url_prefix = "/api/v1/rooms/"

    def test_rooms(self, client):
        user = UserFactory.create()
        RoomFactory.create_batch(5, owner=user)

        response = client.get("/api/v1/rooms/")
        data = json_response(response)

        assert response.status_code == 200
        assert isinstance(data, list)
        assert len(data) == 5

        expected_keys = ['pk', 'name', 'country', 'city', 'price', 'rating', 'is_owner', 'photos']
        got_keys = list(data[0].keys())
        assert all(k in expected_keys for k in got_keys)
