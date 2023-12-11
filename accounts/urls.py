from django.urls import path
from . import views

urlpatterns = [
    path("/sign-up", views.SignUp.as_view()),
    path("/sign-in", views.SignIn.as_view()),
    path("/sign-out", views.SignOut.as_view()),
    path("/change-password", views.ChangePassword.as_view()),
]
