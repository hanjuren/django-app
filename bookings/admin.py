from django.contrib import admin
from .models import Booking


class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "kind",
        "user",
        "room",
        "experience",
        "check_in_at",
        "check_out_at",
        "experience_time",
        "guests",
        "created_at",
        "updated_at",
    )
    list_filter = ("kind",)


admin.site.register(Booking, BookingAdmin)
