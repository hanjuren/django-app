import pytest


pytestmark = pytest.mark.django_db


class TestAmenity:
    def test_str(self, amenity_factory):
        amenity = amenity_factory.create(name="Test Amenity")
        assert str(amenity) == "Test Amenity"
