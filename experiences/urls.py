from django.urls import path
from . import views

urlpatterns = [
    path("/perks", views.Perks.as_view()),
    path("/perks/<int:id_>", views.PerkDetail.as_view()),
]
