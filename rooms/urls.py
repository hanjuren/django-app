from django.urls import path
from . import views

urlpatterns = [
    # path("", views.see_all_rooms),
    # path("<int:id_>", views.see_one_room),
    # path("<str:name>", views.see_one_order),
    path("amenities", views.Amenities.as_view()),
    path("amenities/<int:id_>", views.AmenityDetail.as_view()),
]
