import pytest
import re
from rooms.models import Room, Amenity

pytestmark = pytest.mark.django_db


# GET /api/v1/rooms
class TestGetRooms:
    @pytest.fixture(autouse=True)
    def setup(self, client, room_factory):
        self.client = client
        self.url = "/api/v1/rooms"
        for i in range(5):
            room_factory.create()

    def test_get_rooms(self):
        res = self.client.get(self.url)
        json_response = res.json()

        assert res.status_code == 200
        assert json_response["total"] == 5

        expected_keys = {
            'id',
            'name',
            'country',
            'city',
            'price',
            'user_id',
            'created_at',
            'updated_at',
            "rating",
            "is_owner",
        }
        assert set(json_response['records'][0].keys()) == expected_keys


# POST /api/v1/rooms
class TestPostRoom:
    @pytest.fixture(autouse=True)
    def setup(self, client, user_factory, category_factory):
        self.client = client
        self.url = "/api/v1/rooms"
        self.user = user_factory.create()
        self.category = category_factory.create()
        self.params = {
            "name": "test rooms",
            "country": "korea",
            "city": "seoul",
            "price": 100_000,
            "rooms": 2,
            "toilets": 1,
            "description": None,
            "address": "249, Dongho-ro, Jung-gu, Seoul, Republic of Korea",
            "pet_friendly": False,
            "kind": "private_place",
            "category_id": self.category.id,
        }

    def test_is_authenticated(self):
        res = self.client.post(
            self.url,
            self.params,
        )
        assert res.status_code == 401

    def test_required_filed(self):
        del self.params['name']

        res = self.client.post(
            self.url,
            self.params,
            self.user,
        )
        assert res.status_code == 400

    def test_category_is_not_found(self):
        self.params['category_id'] = -1

        res = self.client.post(
            self.url,
            self.params,
            self.user,
        )
        assert res.status_code == 404

    def test_category_kind_is_not_rooms(self):
        self.category.kind = 'experiences'
        self.category.save()

        res = self.client.post(
            self.url,
            self.params,
            self.user,
        )
        assert res.status_code == 400
        assert res.json().get('message') == "The Category kind should be 'rooms'"

    def test_create_rooms(self):
        before_count = Room.objects.count()
        assert before_count == 0

        res = self.client.post(
            self.url,
            self.params,
            self.user,
        )
        assert res.status_code == 201
        assert Room.objects.count() == 1


# GET /api/v1/rooms/1
class TestGetRoom:
    @pytest.fixture(autouse=True)
    def setup(self, client, room_factory):
        self.client = client
        self.room = room_factory.create()
        self.url = f"/api/v1/rooms/{self.room.id}"

    def test_record_not_found(self):
        res = self.client.get("/api/v1/rooms/-1")
        assert res.status_code == 404

    def test_get_room(self):
        res = self.client.get(self.url)
        json_response = res.json()

        assert res.status_code == 200
        assert json_response["id"] == self.room.id
        assert set(json_response.keys()).issubset(
            {
                "id",
                "name",
                "country",
                "city",
                "price",
                "rooms",
                "toilets",
                "description",
                "address",
                "pet_friendly",
                "kind",
                "user_id",
                "category_id",
                "created_at",
                "updated_at",
                "user",
                "amenities",
                "category",
                "rating",
                "is_owner",
            }
        )


# PUT /api/v1/rooms/1
class TestPutRoom:
    @pytest.fixture(autouse=True)
    def setup(self, client, room_factory, user_factory, category_factory):
        self.client = client
        self.user1 = user_factory.create()
        self.user2 = user_factory.create()
        self.room = room_factory.create(user=self.user1)
        self.url = f"/api/v1/rooms/{self.room.id}"
        self.category = category_factory.create()

    def test_is_authenticate(self):
        res = self.client.put(self.url)
        assert res.status_code == 401

    def test_permission_denied(self):
        res = self.client.put(self.url, None, self.user2)
        assert res.status_code == 403

    def test_put_room(self):
        res = self.client.put(
            self.url,
            {
                "name": "test rooms",
                "country": "korea",
                "city": "seoul",
                "price": 100_000,
                "rooms": 2,
                "toilets": 1,
                "description": None,
                "address": "249, Dongho-ro, Jung-gu, Seoul, Republic of Korea",
                "pet_friendly": False,
                "kind": "private_place",
                "category_id": self.category.id,
            },
            self.user1,
        )

        assert res.status_code == 200


# DELETE /api/v1/rooms/1
class TestDeleteRoom:
    @pytest.fixture(autouse=True)
    def setup(self, client, user_factory, room_factory):
        self.client = client
        self.user1 = user_factory.create()
        self.user2 = user_factory.create()
        self.room = room_factory.create(user=self.user1)
        self.url = f"/api/v1/rooms/{self.room.id}"

    def test_is_authenticate(self):
        res = self.client.delete(self.url)
        assert res.status_code == 401

    def test_permission_denied(self):
        res = self.client.delete(self.url, None, self.user2)
        assert res.status_code == 403

    def test_delete_room(self):
        previous_count = Room.objects.count()
        assert previous_count == 1

        res = self.client.delete(self.url, None, self.user1)
        assert res.status_code == 204
        assert Room.objects.count() == previous_count - 1


# GET /api/v1/rooms/1/reviews
class TestGetRoomReviews:
    @pytest.fixture(autouse=True)
    def setup(self, client, room_factory, review_factory):
        self.client = client
        self.room = room_factory.create()
        self.url = f"/api/v1/rooms/{self.room.id}/reviews"

        for i in range(2):
            review_factory(room=self.room)

    def test_get_room_reviews(self):
        res = self.client.get(self.url)
        json_response = res.json()

        assert res.status_code == 200
        assert json_response["total"] == 2
        assert len(json_response["records"]) == 2


# GET /api/v1/rooms/amenities
class TestGetAmenities:
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
class TestPostAmenities:
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


# GET /api/v1/rooms/amenities/1
class TestGetAmenity:
    @pytest.fixture(autouse=True)
    def setup(self, client, amenity_factory):
        self.client = client
        self.amenity = amenity_factory.create()
        self.url = f"/api/v1/rooms/amenities/{self.amenity.id}"

    def test_record_not_found(self):
        res = self.client.get("/api/v1/rooms/amenities/-1")
        assert res.status_code == 404

    def test_get_amenity(self):
        res = self.client.get(self.url)
        json_response = res.json()

        assert res.status_code == 200
        assert json_response["id"] == self.amenity.id
        assert set(json_response.keys()).issubset(
            {
                "id",
                "name",
                "description",
                "created_at",
                "updated_at",
            }
        )


# PUT /api/v1/rooms/amenities/1
class TestPutAmenity:
    @pytest.fixture(autouse=True)
    def setup(self, client, amenity_factory):
        self.client = client
        self.amenity = amenity_factory.create()
        self.url = f"/api/v1/rooms/amenities/{self.amenity.id}"

    def test_record_not_found(self):
        res = self.client.put("/api/v1/rooms/amenities/-1")
        assert res.status_code == 404

    def test_required_data(self):
        res = self.client.put(self.url)
        json_response = res.json()

        assert res.status_code == 422
        assert "name" in json_response.keys()
        assert re.match("이 필드는 필수 항목입니다.", json_response["name"][0])

    def test_update_amenity(self):
        res = self.client.put(
            self.url,
            {
                "name": "update name",
                "description": "update description"
            }
        )
        json_response = res.json()

        assert res.status_code == 200
        assert json_response["name"] == "update name"
        assert json_response["description"] == "update description"


# DELETE /api/v1/rooms/amenities/1
class TestDeleteAmenity:
    @pytest.fixture(autouse=True)
    def setup(self, client, amenity_factory):
        self.client = client
        self.amenity = amenity_factory.create()
        self.url = f"/api/v1/rooms/amenities/{self.amenity.id}"

    def test_record_not_found(self):
        res = self.client.delete("/api/v1/rooms/amenities/-1")
        assert res.status_code == 404

    def test_delete_amenity(self):
        previous_count = Amenity.objects.count()

        res = self.client.delete(self.url)

        assert res.status_code == 204
        assert Amenity.objects.count() == previous_count - 1
