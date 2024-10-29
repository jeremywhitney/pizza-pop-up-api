from rest_framework import serializers
from ..models import PizzaTopping, Product
from .category_serializer import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "description",
            "category",
            "image_path",
        ]

    def to_representation(self, instance):
        """When reading, return the full category object"""
        ret = super().to_representation(instance)
        ret["category"] = CategorySerializer(instance.category).data
        return ret

    def to_internal_value(self, data):
        """When writing, expect the category as an ID"""
        if isinstance(data.get("category"), dict):
            data["category"] = data["category"].get("id")
        return super().to_internal_value(data)


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price"]


# Associates toppings with an 'OrderProduct'
class PizzaToppingSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="topping.id")
    name = serializers.CharField(source="topping.name")
    price = serializers.FloatField(source="topping.price")

    class Meta:
        model = PizzaTopping
        fields = ["id", "name", "price"]
