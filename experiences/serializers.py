from rest_framework import serializers, exceptions
from . import models
from categories.serializers import CategorySerializer
from categories.models import Category
from users.serializers import TinyUserSerializer


class PerkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Perk
        fields = "__all__"


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Experience
        fields = (
            "pk",
            "description",
            "country",
            "price",
            "city",
            "host",
            "address",
            "starts_at",
            "ends_at",
            "perks",
            "category",
        )

    perks = PerkSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    host = TinyUserSerializer(read_only=True)


class ExperienceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Experience
        fields = (
            "pk",
            "name",
            "description",
            "country",
            "price",
            "city",
            "address",
            "starts_at",
            "ends_at",
            "perks",
            "category",
            "category_id",
            "perk_ids",
            "host",
        )

    perks = PerkSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    host = TinyUserSerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    perk_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
    )

    def validate(self, data):
        category_id = data.get("category_id")
        perk_ids = data.get("perk_ids")

        if category_id:
            try:
                category = Category.objects.get(pk=category_id)
                if category.kind != Category.CategoryKindChoices.EXPERIENCES:
                    raise serializers.ValidationError("Category kind should be Experience")
            except Category.DoesNotExist:
                raise exceptions.NotFound("Not Found")
        else:
            if not self.partial:
                raise serializers.ValidationError("Category id is required")

        if perk_ids:
            if not hasattr(perk_ids, "__len__"):
                raise exceptions.ValidationError("perk_ids is not array.")
            del data["perk_ids"]

        return data
