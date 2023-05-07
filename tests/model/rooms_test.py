import pytest


pytestmark = pytest.mark.django_db


class TestRoom:
    def test_str(self, room_factory):
        room = room_factory.create(name="Test Room...")
        assert str(room) == "Test Room..."
