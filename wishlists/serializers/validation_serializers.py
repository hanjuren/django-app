from rest_framework import serializers
from wishlists.models import Wishlist


class WishlistCreationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)

    def create(self, validated_data):
        return Wishlist.objects.create(**validated_data)


class WishlistUpdateSerializer(WishlistCreationSerializer):
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
