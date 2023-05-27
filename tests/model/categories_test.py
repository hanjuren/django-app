import pytest


pytestmark = pytest.mark.django_db


class TestCategory:
    def test_str(self, category_factory):
        category = category_factory.create()
        assert str(category) == "Test Rooms Category"
