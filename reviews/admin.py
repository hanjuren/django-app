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


class RatingFilter(admin.SimpleListFilter): # noqa
    title = "Filter by Rating"
    parameter_name = "filter_condition"

    FILTER_SET = {
        "good": "rating__gte",
        "bad": "rating__lt",
    }

    def lookups(self, request, model_admin):
        return [
            ("good", "Good Reviews"),
            ("bad", "Bad Reviews"),
        ]

    def queryset(self, request, reviews):
        condition = self.value()
        if condition:
            filter_set = {self.FILTER_SET[condition]: 3}
            return reviews.filter(**filter_set)
        else:
            return reviews


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = ("__str__", "payload", "created_at", "updated_at")
    list_filter = (
        RatingFilter,
        WordFilter,
        "rating",
        "user__is_host",
        "room__category",
        "room__pet_friendly",
    )
