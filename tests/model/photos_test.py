import pytest
import boto3
import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from medias.models import Photo


pytestmark = pytest.mark.django_db


class TestPhoto:
    file_path = os.path.join(settings.BASE_DIR, 'tests', 'fixtures', 'ror.png')

    def test_str(self):
        photo = Photo()
        assert str(photo) == "Photo file"

    def test_initialize_s3_resource(self):
        s3 = Photo.initialize_s3_resource()
        assert isinstance(s3, boto3.resources.base.ServiceResource)

    def test_upload_image(self):
        with open(self.file_path, 'rb') as file:
            file_content = file.read()
            f = SimpleUploadedFile('ror.png', file_content, content_type="image/png")
            result = Photo.upload_image(f)

            assert result.startswith(settings.IMAGE_URL) == True
            assert isinstance(result, str)

            Photo.delete_image(result.replace(f"{settings.IMAGE_URL}/", ""))

    def test_delete_image(self):
        with open(self.file_path, 'rb') as file:
            file_content = file.read()
            f = SimpleUploadedFile('ror.png', file_content, content_type="image/png")
            object_path = Photo.upload_image(f)

            key = object_path.replace(f"{settings.IMAGE_URL}/", "")

            Photo.delete_image(key)
            s3 = Photo.initialize_s3_resource()
            obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, key)

            with pytest.raises(Exception) as error:
                obj.get()

            assert "The specified key does not exist" in str(error.value)
