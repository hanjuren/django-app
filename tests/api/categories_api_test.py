import pytest
import re
from categories.models import Category


pytestmark = pytest.mark.django_db


# GET /api/v1/categories
class TestGetCategories:
    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.client = client
        self.url = "/api/v1/categories"

    def test_get_categories(self, category_factory):
        for i in range(5):
            category_factory.create(name=f"Test Category{i + 1}")

        res = self.client.get(self.url)
        json_response = res.json()

        assert res.status_code == 200
        print(json_response)
        assert json_response["total"] == 5
        assert len(json_response["records"]) == 5

        expected_keys = {"id", "name", "kind", "created_at", "updated_at"}
        assert set(json_response["records"][0].keys()).issubset(expected_keys)


# POST /api/v1/categories
class TestPostCategories:
    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.client = client
        self.url = "/api/v1/categories"

    def test_required_data(self):
        res = self.client.post(
            self.url,
            {
                "kind": "rooms",
            }
        )
        json_response = res.json()

        assert res.status_code == 422
        assert "name" in json_response.keys()
        assert re.match("이 필드는 필수 항목입니다.", json_response["name"][0])

        res = self.client.post(
            self.url,
            {
                "name": "test name",
            }
        )
        json_response = res.json()

        assert res.status_code == 422
        assert "kind" in json_response.keys()
        assert re.match("이 필드는 필수 항목입니다.", json_response["kind"][0])

    def test_invalid_choice_value(self):
        res = self.client.post(
            self.url,
            {
                "name": "test name",
                "kind": "xxx",
            }
        )
        json_response = res.json()

        assert res.status_code == 422
        assert re.match(r'"xxx"이 유효하지 않은 선택\(choice\)입니다.', json_response["kind"][0])

    def test_create(self):
        previous_count = Category.objects.count()

        res = self.client.post(
            self.url,
            {
                "name": "test name",
                "kind": "rooms",
            }
        )
        json_response = res.json()

        assert res.status_code == 201
        assert json_response["name"] == "test name"
        assert json_response["kind"] == "rooms"
        assert Category.objects.count() == previous_count + 1


# GET /api/v1/categories/1
class TestGetCategory:
    @pytest.fixture(autouse=True)
    def setup(self, client, category_factory):
        self.client = client
        self.category = category_factory.create()
        self.url = f"/api/v1/categories/{self.category.id}"

    def test_record_not_found(self):
        res = self.client.get("/api/v1/categories/-1")
        assert res.status_code == 404

    def test_get_category(self):
        res = self.client.get(self.url)
        json_response = res.json()

        assert res.status_code == 200
        assert json_response["id"] == self.category.id

        expected_keys = {"id", "name", "kind", "created_at", "updated_at"}
        assert set(json_response.keys()).issubset(expected_keys)


# PUT /api/v1/categories/1
class TestPutAmenity:
    @pytest.fixture(autouse=True)
    def setup(self, client, category_factory):
        self.client = client
        self.category = category_factory.create()
        self.url = f"/api/v1/categories/{self.category.id}"

    def test_required_data(self):
        res = self.client.put(
            self.url,
            {
                "name": "update name",
            }
        )
        json_response = res.json()

        assert res.status_code == 422
        assert re.match("이 필드는 필수 항목입니다.", json_response["kind"][0])

    def test_update(self):
        res = self.client.put(
            self.url,
            {
                "name": self.category.name,
                "kind": "experiences",
            }
        )
        json_response = res.json()

        assert res.status_code == 200
        assert json_response["kind"] == "experiences"


# DELETE /api/v1/categories/1
class TestDeleteCategory:
    @pytest.fixture(autouse=True)
    def setup(self, client, category_factory):
        self.client = client
        self.category = category_factory.create()
        self.url = f"/api/v1/categories/{self.category.id}"

    def test_delete(self):
        previous_count = Category.objects.count()

        res = self.client.delete(self.url)

        assert res.status_code == 204
        assert Category.objects.count() == previous_count - 1
