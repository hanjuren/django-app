from django.contrib import admin
from .models import Wishlist


class WishlistAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "created_at",
        "updated_at",
    )


admin.site.register(Wishlist, WishlistAdmin)
