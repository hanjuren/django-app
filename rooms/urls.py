from django.urls import path
from . import views

urlpatterns = [
    path("", views.Rooms.as_view()),
    path("/<int:id_>", views.RoomDetail.as_view()),
    path("/<int:id_>/reviews", views.RoomReviews.as_view()),
    path("/<int:id_>/photos", views.RoomPhotos.as_view()),
    # path("<str:name>", views.see_one_order),
    path("/amenities", views.Amenities.as_view()),
    path("/amenities/<int:id_>", views.AmenityDetail.as_view()),
]
