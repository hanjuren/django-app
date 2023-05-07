import pytest


pytestmark = pytest.mark.django_db


class TestPerk:
    def test_str(self, perk_factory):
        perk = perk_factory.create(name="Test Perk")
        assert str(perk) == "Test Perk"
