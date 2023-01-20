from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views


urlpatterns = [
    path("", views.Users.as_view()),
    path("me/", views.Me.as_view()),
    path("change-password/", views.ChangePassword.as_view()),
    path("sign-in/", views.SignIn.as_view()),
    path("sign-out/", views.SignOut.as_view()),
    path("token-login/", obtain_auth_token),
    path("@<str:username>/", views.PublicUser.as_view()),
]