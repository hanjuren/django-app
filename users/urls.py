from django.urls import path
from . import views


urlpatterns = [
    # /api/v1/users/
    path("", views.Users.as_view()),
    # /api/v1/users/me/
    path("me/", views.Me.as_view()),
    # /api/v1/users/password
    path("password/", views.ChangePassword.as_view()),
    # /api/v1/sign_up
    path("sign_in/", views.SignIn.as_view()),
    path("sign-out/", views.SignOut.as_view()),

    path("@<str:username>/", views.PublicUser.as_view()),
]