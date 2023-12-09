from django.urls import path
from . import views

urlpatterns = [
    path("", views.Users.as_view()),
    path("/<int:pk>", views.UserDetail.as_view()),
    path("/<int:pk>/change-password", views.ChangePassword.as_view()),
    path("/<int:pk>/avatar", views.Avatar.as_view()),
    path("/sign-in", views.SignIn.as_view()),
    path("/sign-out", views.SignOut.as_view()),
]
