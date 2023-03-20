from django.urls import path
from . import views

urlpatterns = [
    # /api/v1/auth/sign_up/
    path("sign_up/", views.SignUp.as_view()),
]
