from rest_framework import serializers
from ..models.order_product import OrderProduct
from .product_serializer import PizzaToppingSerializer


class LineItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="product.id", read_only=True)
    name = serializers.CharField(source="product.name", read_only=True)
    price = serializers.FloatField(source="product.price", read_only=True)
    toppings = PizzaToppingSerializer(
        source="pizza_toppings", many=True, read_only=True
    )

    class Meta:
        model = OrderProduct
        fields = ["id", "name", "price", "quantity", "toppings"]

    def to_representation(self, instance):
        """Customize the output to include flattened product info and toppings"""
        representation = super().to_representation(instance)
        return representation
