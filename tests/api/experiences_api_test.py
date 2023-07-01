import pytest
import re
from experiences.models import Perk


pytestmark = pytest.mark.django_db


class TestGetPerks:
    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.client = client
        self.url = "/api/v1/experiences/perks"

    def test_get_perks(self, perk_factory):
        for i in range(3):
            perk_factory.create()

        res = self.client.get(self.url)
        json_response = res.json()

        assert res.status_code == 200
        assert json_response["total"] == 3
        assert len(json_response["records"]) == 3

        expected_keys = {"id", "name", "detail", "description", "created_at", "updated_at"}
        assert set(json_response["records"][0].keys()).issubset(expected_keys)


class TestPostPerks:
    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.client = client
        self.url = "/api/v1/experiences/perks"

    def test_required_data(self):
        res = self.client.post(
            self.url,
            {
                "name": "Test Perk name",
                "detail": "Test Perk detail",
            }
        )
        json_response = res.json()

        assert res.status_code == 422
        assert re.match("이 필드는 필수 항목입니다.", json_response["description"][0])

    def test_create(self):
        previous_count = Perk.objects.count()

        res = self.client.post(
            self.url,
            {
                "name": "Test Perk name",
                "detail": "Test Perk detail",
                "description": "Test Perk description",
            }
        )
        json_response = res.json()

        assert res.status_code == 201
        assert Perk.objects.count() == previous_count + 1
