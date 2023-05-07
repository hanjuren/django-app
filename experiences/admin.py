from django.contrib import admin
from .models import Experience, Perk


class ExperienceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "country",
        "city",
        "price",
        "started_at",
        "finished_at",
        "user_id",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "city",
        "started_at",
        "finished_at",
    )


class PerkAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "detail",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "created_at",
    )


admin.site.register(Experience, ExperienceAdmin)
admin.site.register(Perk, PerkAdmin)
