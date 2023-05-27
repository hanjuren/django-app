import pytest


pytestmark = pytest.mark.django_db


class TestBooking:
    def test_str(self, create_booking, user_factory, room_factory):
        user = user_factory.create(name="Mike")
        room = room_factory.create()
        booking = create_booking('room', user.id, 2, room.id)
        assert str(booking) == f"Room booking for: Mike"
