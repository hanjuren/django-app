import pytest


pytestmark = pytest.mark.django_db


class TestWishlist:
    def test_str(self, wishlist_factory):
        wishlist = wishlist_factory.create(name="Trip to Seoul")
        assert str(wishlist) == "Trip to Seoul"
