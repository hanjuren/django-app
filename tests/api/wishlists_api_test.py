import pytest
from wishlists.models import Wishlist

pytestmark = pytest.mark.django_db


class TestGetWishlists:
    @pytest.fixture(autouse=True)
    def setup(self, client, user_factory, wishlist_factory):
        self.client = client
        self.user = user_factory.create()
        self.wishlist = wishlist_factory.create(user=self.user)

    def test_is_authenticated(self):
        res = self.client.get("/api/v1/wishlists")
        assert res.status_code == 401

    def test_get_wishlists(self):
        res = self.client.get("/api/v1/wishlists", user=self.user)

        assert res.status_code == 200
        expected_keys = {
            "id",
            "name",
            "user_id",
            "rooms",
            "created_at",
            "updated_at",
        }
        assert set(res.json()['records'][0].keys()) == expected_keys


class TestPostWishlist:
    @pytest.fixture(autouse=True)
    def setup(self, client, user_factory):
        self.client = client
        self.user = user_factory.create()

    def test_is_authenticated(self):
        res = self.client.post("/api/v1/wishlists")
        assert res.status_code == 401

    def test_validation_error(self):
        res = self.client.post("/api/v1/wishlists", user=self.user)
        assert res.status_code == 400

    def test_create_wishlist(self):
        res = self.client.post(
            "/api/v1/wishlists",
            data={"name": "test wishlist"},
            user=self.user
        )
        assert res.status_code == 201


class TestGetWishlist:
    @pytest.fixture(autouse=True)
    def setup(self, client, user_factory, wishlist_factory):
        self.client = client
        self.user = user_factory.create()
        self.wishlist = wishlist_factory.create(user=self.user)

    def test_is_authenticated(self):
        res = self.client.get(f"/api/v1/wishlists/{self.wishlist.id}")
        assert res.status_code == 401

    def test_get_wishlist(self):
        res = self.client.get(f"/api/v1/wishlists/{self.wishlist.id}", user=self.user)
        assert res.status_code == 200


class TestPutWishlist:
    @pytest.fixture(autouse=True)
    def setup(self, client, user_factory, wishlist_factory):
        self.client = client
        self.user = user_factory.create()
        self.wishlist = wishlist_factory.create(user=self.user)

    def test_is_authenticated(self):
        res = self.client.put(f"/api/v1/wishlists/{self.wishlist.id}")
        assert res.status_code == 401

    def test_update_wishlist(self):
        res = self.client.put(
            f"/api/v1/wishlists/{self.wishlist.id}",
            data={"name": "wishlist update test"},
            user=self.user
        )
        assert res.status_code == 200
        assert res.json()['name'] == "wishlist update test"

class TestDeleteWishlist:
    @pytest.fixture(autouse=True)
    def setup(self, client, user_factory, wishlist_factory):
        self.client = client
        self.user = user_factory.create()
        self.wishlist = wishlist_factory.create(user=self.user)

    def test_is_authenticated(self):
        res = self.client.delete(f"/api/v1/wishlists/{self.wishlist.id}")
        assert res.status_code == 401

    def test_update_wishlist(self):
        previous_count = Wishlist.objects.count()

        res = self.client.delete(f"/api/v1/wishlists/{self.wishlist.id}", user=self.user)
        assert res.status_code == 204
        assert Wishlist.objects.count() == previous_count - 1
