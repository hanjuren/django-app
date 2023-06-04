from django.contrib import admin
from .models import Room, Amenity


@admin.action(description="Set all prices to zero")
def reset_prices(model_admin, request, rooms):
    rooms.update(price=0)


class RoomAdmin(admin.ModelAdmin):
    actions = (reset_prices,)

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
    search_fields = (
        "^name",
        "=price",
        "user__name",
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
