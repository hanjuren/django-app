import pytest


pytestmark = pytest.mark.django_db


class TestExperience:
    def test_str(self, experience_factory):
        experience = experience_factory.create(name="Test Experience")
        assert str(experience) == "Test Experience"
