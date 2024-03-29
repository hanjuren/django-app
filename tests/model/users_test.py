import os
import pytest
import jwt
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from config.s3 import PublicS3
from users.models import User


pytestmark = pytest.mark.django_db


class TestUser:
    def teardown_method(self):
        User.objects.all().delete()

    def test_create_user_value_error(self):
        with pytest.raises(ValueError, match="Users must have an email address"):
            User.objects.create_user("", "test user")

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

    def test_upload_avatar(self, user_factory):
        user = user_factory.create()
        file_path = os.path.join(settings.BASE_DIR, 'tests', 'fixtures', 'ror.png')

        with open(file_path, 'rb') as file:
            file_content = file.read()
            f = SimpleUploadedFile('ror.png', file_content, content_type="image/png")
            result = user.upload_avatar(f)
            user.avatar = result
            user.save()

            assert user.avatar.startswith(settings.IMAGE_URL) == True
            assert isinstance(user.avatar, str)

    def test_delete_avatar(self, user_factory):
        user = user_factory.create()
        file_path = os.path.join(settings.BASE_DIR, 'tests', 'fixtures', 'ror.png')
        with open(file_path, 'rb') as file:
            file_content = file.read()
            f = SimpleUploadedFile('ror.png', file_content, content_type="image/png")
            result = user.upload_avatar(f)
            user.avatar = result
            user.save()

        key = user.avatar.replace(f"{settings.IMAGE_URL}/", "")
        user.delete_avatar()

        s3 = PublicS3()
        obj = s3.resource.Object(settings.AWS_STORAGE_BUCKET_NAME, key)
        with pytest.raises(Exception) as error:
            obj.get()
        assert "The specified key does not exist" in str(error.value)


    def test_is_superuser(self, user_factory):
        user1 = user_factory.create()
        assert user1.is_superuser is False

        user2 = user_factory.create(is_admin=True)
        assert user2.is_superuser is True

    def test_generate_token(self, user_factory):
        user = user_factory.create()
        token = jwt.decode(user.generate_token(), settings.JWT_SECRET_KEY, algorithms=['HS256'])

        assert token['user_id'] == user.id
        assert token['user_email'] == user.email
        assert token['user_name'] == user.name
        assert token['user_is_admin'] == user.is_admin
