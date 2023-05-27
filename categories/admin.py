from django.contrib import admin
from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "kind",
        "created_at",
        "updated_at",
    )
    list_filter = ("kind",)


admin.site.register(Category, CategoryAdmin)
