from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ("pk", "name", "kind", "created_at", "updated_at")
    list_filter = ("kind",)
