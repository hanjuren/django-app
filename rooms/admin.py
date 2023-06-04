from django.contrib import admin
from .models import Room, Amenity


class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "kind",
        "user_id",
        "total_amenities",
        "reviews_rating",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "country",
        "kind",
    )


class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "name",
        "created_at",
    )


admin.site.register(Room, RoomAdmin)
admin.site.register(Amenity, AmenityAdmin)
