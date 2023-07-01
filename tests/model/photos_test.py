import pytest
from medias.models import Photo


pytestmark = pytest.mark.django_db


class TestPhoto:
    def test_str(self):
        photo = Photo()
        assert str(photo) == "Photo file"
