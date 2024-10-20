from rest_framework import serializers
from ..models import PizzaTopping, Product
from .category_serializer import CategorySerializer


# Base product details
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

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

class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']


# Simplified 'Product' details for toppings
class ToppingSerializer(serializers.ModelSerializer):
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
