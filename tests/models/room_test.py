import pytest

pytestmark = pytest.mark.django_db


class TestRoom:
    @pytest.fixture(autouse=True)
    def set_up(self, user_factory, room_factory):
        self.user = user_factory.create()
        self.room = room_factory.create(
            name="테스트 룸",
            owner=self.user
        )

    def test_total_amenities(self, amenity_factory):
        assert self.room.total_amenities() == 0

        amenity = amenity_factory.create()
        self.room.amenities.add(amenity)

        assert self.room.total_amenities() == 1

    def test_rating(self, review_factory):
        assert self.room.rating() == 0

        review = review_factory.create(
            user=self.user,
            room=self.room,
        )

        assert self.room.rating() == 4

    def test_add_amenities(self, amenity_factory):
        amenity_ids = []
        for name in ["test amenity 1", "test amenity 2"]:
            amenity = amenity_factory.create(name=name)
            amenity_ids.append(amenity.pk)
        self.room.add_amenities(amenity_ids)

        assert self.room.amenities.count() == 2

        # duplicate amenity add is not working
        self.room.add_amenities(amenity_ids[0:1])

        assert self.room.amenities.count() != 3
        assert self.room.amenities.count() == 2
