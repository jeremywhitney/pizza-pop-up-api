from rest_framework import serializers
from ..models.product import Product


class ProductSerializer(serializers.ModelSerializer):
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
