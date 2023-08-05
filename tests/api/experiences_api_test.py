import pytest
import re
from experiences.models import Perk


pytestmark = pytest.mark.django_db


# GET /api/v1/experiences/perks
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


# POST /api/v1/experiences/perks
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
        assert json_response["name"] == 'Test Perk name'
        assert json_response["detail"] == 'Test Perk detail'
        assert json_response["description"] == 'Test Perk description'


# GET /api/v1/experiences/perks/1
class TestGetPerk:
    @pytest.fixture(autouse=True)
    def setup(self, client, perk_factory):
        self.client = client
        self.perk = perk_factory.create()
        self.url = f"/api/v1/experiences/perks/{self.perk.id}"

    def test_record_not_found(self):
        res = self.client.get("/api/v1/experiences/perks/-1")
        assert res.status_code == 404

    def test_get_perk(self):
        res = self.client.get(self.url)
        json_response = res.json()

        assert res.status_code == 200
        assert json_response["id"] == self.perk.id

        expected_keys = {"id", "name", "detail", "description", "created_at", "updated_at"}
        assert set(json_response.keys()).issubset(expected_keys)


# PUT /api/v1/experiences/perks/1
class TestPutPerk:
    @pytest.fixture(autouse=True)
    def setup(self, client, perk_factory):
        self.client = client
        self.perk = perk_factory.create()
        self.url = f"/api/v1/experiences/perks/{self.perk.id}"

    def test_required_data(self):
        res = self.client.put(
            self.url,
            {
                "name": "update name",
                "description": "update detail"
            }
        )
        json_response = res.json()

        assert res.status_code == 422
        assert re.match("이 필드는 필수 항목입니다.", json_response["detail"][0])

    def test_update(self):
        res = self.client.put(
            self.url,
            {
                "name": "update name",
                "detail": "update detail",
                "description": self.perk.description
            }
        )
        json_response = res.json()

        assert res.status_code == 200
        assert json_response["name"] == 'update name'
        assert json_response["detail"] == 'update detail'
        assert json_response["description"] == self.perk.description


# DELETE /api/v1/experiences/perks/1
class TestDeletePerk:
    @pytest.fixture(autouse=True)
    def setup(self, client, perk_factory):
        self.client = client
        self.perk = perk_factory.create()
        self.url = f"/api/v1/experiences/perks/{self.perk.id}"

    def test_delete(self):
        previous_count = Perk.objects.count()

        res = self.client.delete(self.url)

        assert res.status_code == 204
        assert Perk.objects.count() == previous_count - 1
