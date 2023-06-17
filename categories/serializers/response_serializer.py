from rest_framework import serializers


class CategoryResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(required=True)
    kind = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
