import pytest
from users.models import User


pytestmark = pytest.mark.django_db


class TestUser:
    def test_create_user(self):
        user = User.objects.create_user(
            "juren528@gmail.com",
            "Test User",
        )
        assert User.objects.count() == 1
        assert user.email == "juren528@gmail.com"
        assert user.name == "Test User"
        assert user.is_admin is False

    def test_create_super_user(self):
        super_user = User.objects.create_superuser(
            "juren528@gmail.com",
            password="password12",
            name="Test User",
        )
        assert User.objects.count() == 1
        assert super_user.email == "juren528@gmail.com"
        assert super_user.password is not None
        assert super_user.name == "Test User"
        assert super_user.is_admin is True
