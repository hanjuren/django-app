import pytest
from tests.factories import *
from users.models import User

pytestmark = pytest.mark.django_db


class TestRoom:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.user = UserFactory.create()
        self.room = RoomFactory.create(
            name="테스트 룸",
            owner=self.user
        )

    def test_total_amenities(self):
        assert self.room.total_amenities() == 0

        amenity = AmenityFactory.create()
        self.room.amenities.add(amenity)

        assert self.room.total_amenities() == 1

    def test_rating(self):
        assert self.room.rating() == 0

        review = ReviewFactory.create(
            user=self.user,
            room=self.room,
        )

        assert self.room.rating() == 4
