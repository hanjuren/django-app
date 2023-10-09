import pytest
from medias.models import Photo

pytestmark = pytest.mark.django_db


class TestDeletePhoto:
    @pytest.fixture(autouse=True)
    def setup(self, client, photo_factory, room_factory, user_factory):
        self.client = client

        self.current_user = user_factory.create()
        self.another_user = user_factory.create()
        self.room = room_factory.create(user=self.current_user)
        self.photo = photo_factory.create(room=self.room)

    def test_is_authenticated(self):
        res = self.client.delete(f"/api/v1/medias/{self.photo.id}")
        assert res.status_code == 401

    def test_permission_denied(self):
        res = self.client.delete(f"/api/v1/medias/{self.photo.id}", user=self.another_user)
        assert res.status_code == 403

    def test_delete_photo(self):
        previous_count = Photo.objects.count()

        res = self.client.delete(f"/api/v1/medias/{self.photo.id}", user=self.current_user)
        assert res.status_code == 204
        assert Photo.objects.count() == previous_count - 1
