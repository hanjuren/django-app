import pytest
from categories.models import Category
from categories.serializers.validation_serializers import CategoryCreationSerializer, CategoryUpdateSerializer


pytestmark = pytest.mark.django_db


class TestCreationSerializer:
    def test_create(self):
        previous_count = Category.objects.count()
        serializer = CategoryCreationSerializer()
        validated_data = {"name": "Category Serializer Test", "kind": "kind"}

        serializer.create(validated_data)

        assert Category.objects.count() == previous_count + 1


class TestUpdateSerializer:
    def test_update(self, category_factory):
        category = category_factory.create()
        serializer = CategoryUpdateSerializer()
        validated_data = {"name": "Update Test"}

        serializer.update(category, validated_data)

        assert category.name == "Update Test"
