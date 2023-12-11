from django.contrib.auth import logout


class SignOutService:
    def __init__(self, request):
        self.request = request

    def execute(self):
        logout(self.request)