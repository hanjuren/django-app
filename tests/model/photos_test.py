import pytest
from config.s3 import PublicS3
import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from medias.models import Photo


pytestmark = pytest.mark.django_db


class TestPhoto:
    file_path = os.path.join(settings.BASE_DIR, 'tests', 'fixtures', 'ror.png')

    def teardown_method(self):
        Photo.objects.all().delete()

    def test_str(self):
        photo = Photo()
        assert str(photo) == "Photo file"

    def test_upload_image(self, photo_factory):
        with open(self.file_path, 'rb') as file:
            file_content = file.read()
            f = SimpleUploadedFile('ror.png', file_content, content_type="image/png")
            result = Photo.upload_image(f)

            photo = photo_factory.create(file=result)

            assert photo.file.startswith(settings.IMAGE_URL) == True
            assert isinstance(photo.file, str)

    def test_delete_image(self, photo_factory):
        with open(self.file_path, 'rb') as file:
            file_content = file.read()
            f = SimpleUploadedFile('ror.png', file_content, content_type="image/png")
            object_path = Photo.upload_image(f)

            photo = photo_factory.create(file=object_path)
            key = photo.file.replace(f"{settings.IMAGE_URL}/", "")
            photo.delete_image()

            s3 = PublicS3()
            obj = s3.resource.Object(settings.AWS_STORAGE_BUCKET_NAME, key)
            with pytest.raises(Exception) as error:
                obj.get()
            assert "The specified key does not exist" in str(error.value)
