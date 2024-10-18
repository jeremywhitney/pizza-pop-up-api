from rest_framework import serializers
from ..models.product import Product
from .category_serializer import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "description",
            "created_date",
            "category",
            "image_path",
        ]
        read_only_fields = ["id", "created_date"]
