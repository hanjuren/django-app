import pytest
import re
from rooms.models import Amenity

pytestmark = pytest.mark.django_db


class TestRoomAPI:
    pass


# GET /api/v1/room/amenities
class TestGetAmenitiesAPI:
    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.client = client

    def test_get_amenities(self, amenity_factory):
        for i in range(5):
            amenity_factory.create()

        res = self.client.get("/api/v1/rooms/amenities")
        json_response = res.json()

        assert res.status_code == 200
        assert json_response['total'] == 5
        assert len(json_response['records']) == 5

        expected_keys = {'id', 'name', 'description', 'created_at', 'updated_at'}
        assert set(json_response['records'][0].keys()) == expected_keys


# POST /api/v1/rooms/amenities
class TestPostAmenitiesAPI:
    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.client = client
        self.url = "/api/v1/rooms/amenities"

    def test_name_is_required(self):
        res = self.client.post(
            self.url,
            {},
        )
        json_response = res.json()

        assert res.status_code == 422
        assert "name" in json_response.keys()
        assert re.match("이 필드는 필수 항목입니다.", json_response["name"][0])

    def test_create_amenity(self):
        # before
        assert Amenity.objects.count() == 0

        res = self.client.post(
            self.url,
            {
                "name": "create amenity.",
                "description": "create amenity test."
            }
        )
        json_response = res.json()

        assert res.status_code == 201
        assert json_response["name"] == "create amenity."
        assert json_response["description"] == "create amenity test."
        assert Amenity.objects.count() == 1
