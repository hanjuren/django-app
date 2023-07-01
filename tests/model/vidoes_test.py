import pytest
from medias.models import Video


pytestmark = pytest.mark.django_db


class TestVideo:
    def test_str(self):
        video = Video()
        assert str(video) == "Video file"
