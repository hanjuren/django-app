from django.urls import path
from . import views

urlpatterns = [
    path("", views.Users.as_view()),
    path("/me", views.Me.as_view()),
    path("/me/avatar", views.Avatar.as_view()),
]
