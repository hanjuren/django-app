from django.contrib import admin
from .models import Review


class WordFilter(admin.SimpleListFilter):  # noqa
    title = "Filter by Words"
    parameter_name = "word"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("great", "Great"),
            ("awesome", "Awesome"),
        ]

    def queryset(self, request, queryset):
        word = self.value()
        if word:
            result = queryset.filter(payload__contains=word)
            return result
        else:
            result = queryset.all()
            return result


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = ("__str__", "payload", "created_at", "updated_at")
    list_filter = (
        WordFilter,
        "rating",
        "user__is_host",
        "room__category",
        "room__pet_friendly",
    )
