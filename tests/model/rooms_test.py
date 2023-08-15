import pytest


pytestmark = pytest.mark.django_db


class TestRoom:
    def test_str(self, room_factory):
        room = room_factory.create(name="Test Room...")
        assert str(room) == "Test Room..."

    def test_total_amenities(self, room_factory, amenity_factory):
        room = room_factory.create()

        assert room.total_amenities() == 0

        for i in range(2):
            amenity = amenity_factory.create()
            room.amenities.add(amenity)

        assert room.total_amenities() == 2

    def test_reviews_rating(self, room_factory, review_factory):
        room = room_factory.create()

        assert room.reviews_rating() == 0

        for rating in [3, 4]:
            review_factory.create(rating=rating, room=room)

        assert room.reviews_rating() == 3.5

    def test_add_amenities(self, room_factory, amenity_factory):
        room = room_factory.create()
        amenity1 = amenity_factory.create()
        amenity2 = amenity_factory.create()

        before_count = room.amenities.count()
        assert before_count == 0

        room.add_amenities([amenity1.id, amenity2.id])
        room.refresh_from_db()

        assert room.amenities.count() == 2
