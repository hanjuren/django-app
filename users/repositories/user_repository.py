import os
from django.conf import settings
from config.s3 import PublicS3

from users.models import User
from users.repositories.abstracts import AbstractUserRepository


class UserRepository(AbstractUserRepository):
    def create(self, data: dict) -> User:
        user = User(
            email=data.get('email'),
            name=data.get('name'),
            gender=data.get('gender'),
            language=data.get('language'),
            currency=data.get('currency'),
            is_host=data.get('is_host')
        )
        user.set_password(data.get('password'))
        user.save()

        return user

    def get(self, pk: int) -> User:
        return User.objects.get(id=pk)

    def update(self, user: User, data: dict) -> None:
        for attr, value in data.items():
            setattr(user, attr, value)
        user.save()

    def set_password(self, user: User, password: str) -> None:
        user.set_password(password)
        user.save()

    def update_avatar(self, user: User, data) -> None:
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
