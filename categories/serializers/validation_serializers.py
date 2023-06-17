from rest_framework import serializers
from categories.models import Category


class CategoryCreationSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=50)
    kind = serializers.ChoiceField(choices=Category.CategoryKindChoices.choices)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)


class CategoryUpdateSerializer(CategoryCreationSerializer):
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
