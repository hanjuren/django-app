from rest_framework.exceptions import ParseError
from users.models import User


class ChangePasswordService:
    def __init__(self, current_user: User, data: dict):
        self.current_user = current_user
        self.data = data

    def execute(self) -> User:
        self.__check_old_password()
        self.current_user.set_password(self.data['new_password'])
        return self.current_user

    def __check_old_password(self):
        valid = self.current_user.check_password(self.data['old_password'])
        if valid is False:
            raise ParseError("password is not valid.")
