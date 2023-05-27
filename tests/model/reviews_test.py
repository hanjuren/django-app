import pytest


pytestmark = pytest.mark.django_db


class TestReview:
    def test_str(self, review_factory, user_factory, room_factory):
        review = review_factory.create(
            rating=5,
            user=user_factory(name="Test user"),
            room=room_factory()
        )
        assert str(review) == "Test user / 5"
