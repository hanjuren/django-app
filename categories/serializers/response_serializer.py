from rest_framework import serializers
from categories.models import Category


class CategoryResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
