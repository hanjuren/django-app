from django.urls import path
from . import views

urlpatterns = [
    path("", views.all_categories),
    path("<int:id_>", views.get_category),
]
