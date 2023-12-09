from abc import ABC, abstractmethod
from users.models import User


class AbstractUserRepository(ABC):
    @abstractmethod
    def create(self, data: dict) -> User:
        raise NotImplementedError

    @abstractmethod
    def get(self, pk: int) -> User:
        raise NotImplementedError

    @abstractmethod
    def update(self, user: User, data: dict):
        raise NotImplementedError

    @abstractmethod
    def set_password(self, user: User, password: str):
        raise NotImplementedError

    @abstractmethod
    def update_avatar(self, user: User, data: dict):
        raise NotImplementedError

