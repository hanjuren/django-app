from users.models import User


class SignUpService:
    def __init__(self, data):
        self.data = data

    def execute(self):
        User.objects.create(**self.data)
