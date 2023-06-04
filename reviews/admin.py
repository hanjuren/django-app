from django.contrib import admin
from .models import Review


class WordFilter(admin.SimpleListFilter):
    title = "Filter by words."
    parameter_name = "word"

    def lookups(self, request, model_admin) -> list[tuple]:
        return [
            ("good", "Good"),
            ("great", "Great"),
            ("awesome", "Awesome"),
            ("bad", "Bad"),
        ]

    def queryset(self, request, queryset) -> list[Review]:
        word = request.GET.get('word')

        if word:
            return queryset.filter(payload__contains=word)
        else:
            return queryset


class SatisFactionFilter(admin.SimpleListFilter):
    title = "Filter by satisfaction."
    parameter_name = "satisfaction"

    def lookups(self, request, model_admin) -> list[tuple]:
        return [
            ("bad", "Bad Reviews"),
            ("good", "Good Reviews")
        ]

    def queryset(self, request, queryset) -> list[Review]:
        q = queryset
        satisfaction = request.GET.get('satisfaction')

        if satisfaction == "good":
            q = q.filter(rating__gte=3)
        elif satisfaction == "bad":
            q = q.filter(rating__lt=3)

        return q


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "payload",
        "created_at",
        "updated_at",
    )
    list_filter = (
        WordFilter,
        SatisFactionFilter,
    )


admin.site.register(Review, ReviewAdmin)
