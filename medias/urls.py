from django.urls import path
from . import views

urlpatterns = [
    path("/<int:id_>", views.PhotoDetail.as_view()),
]
