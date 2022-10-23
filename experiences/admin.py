from django.contrib import admin
from .models import Experience, Perk


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):

    list_display = ("name", "price", "starts_at", "ends_at", "created_at", "updated_at")
    list_filter = ("category",)


@admin.register(Perk)
class PerkAdmin(admin.ModelAdmin):

    list_display = ("name", "details", "explanation", "created_at", "updated_at")
