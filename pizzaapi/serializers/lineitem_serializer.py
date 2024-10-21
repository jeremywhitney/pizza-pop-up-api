from rest_framework import serializers
from .product_serializer import (
    OrderProductSerializer,
    PizzaToppingSerializer,
)
from ..models.order_product import OrderProduct


class LineItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    # product = serializers.IntegerField()
    toppings = PizzaToppingSerializer(
        source="pizza_toppings", many=True, read_only=True
    )

    class Meta:
        model = OrderProduct
        fields = ["product", "quantity", "toppings"]

    def get_product(self, obj):
        return OrderProductSerializer(obj.product).data

    def to_representation(self, instance):
        """Customize output representation to include product details."""
        representation = super().to_representation(instance)
        representation["product"] = OrderProductSerializer(
            instance.product
        ).data  # Add product details
        return representation
