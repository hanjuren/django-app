from django.urls import path
from . import views

urlpatterns = [
    path("", views.Wishlists.as_view()),
    path("/<int:id_>", views.WishlistDetail.as_view()),
    path("/<int:id_>/rooms/<int:room_id>", views.WishlistRooms.as_view())
]
