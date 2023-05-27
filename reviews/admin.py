from django.contrib import admin
from .models import Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "payload",
        "created_at",
        "updated_at",
    )
    list_filter = ("rating",)


admin.site.register(Review, ReviewAdmin)
