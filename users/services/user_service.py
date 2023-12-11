import os

from django.conf import settings

from config.s3 import PublicS3
from users.models import User


class UserService:
    def get_user(self, pk) -> User:
        return User.objects.get(pk=pk)

    def update_user(self, pk, data) -> User:
        user = User.objects.get(pk=pk)
        user.objects.update(**data)

        return user

    def update_avatar(self, pk, data) -> User:
        user = User.objects.get(pk=pk)

        s3 = PublicS3()
        file = data.get('file')

        if file:
            base_dir = "users/avatar"
            file_name, extension = os.path.splitext(file.name)
            path = f"{base_dir}/{user.id}/{file_name}{extension}"
            s3.put_object(path, file, file.content_type)

            user.avatar = f"{settings.IMAGE_URL}/{path}"
        else:
            key = user.avatar.replace(f"{settings.IMAGE_URL}/", "")
            s3.delete_object(key)
            user.avatar = None

        user.save()

        return user
