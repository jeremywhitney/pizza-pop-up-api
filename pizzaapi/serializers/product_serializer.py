from rest_framework import serializers
from ..models import PizzaTopping, Product
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
            "category",
            "image_path",
        ]


class ToppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price"]


class PizzaToppingSerializer(serializers.ModelSerializer):
    topping = ToppingSerializer()

    class Meta:
        model = PizzaTopping
        fields = ["topping"]


class PizzaWithToppingsSerializer(ProductSerializer):
    toppings = PizzaToppingSerializer(
        source="pizza_toppings", many=True, read_only=True
    )

    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ["toppings"]
