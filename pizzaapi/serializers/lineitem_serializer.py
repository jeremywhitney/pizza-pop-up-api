from rest_framework import serializers
from .product_serializer import ProductSerializer, PizzaWithToppingsSerializer
from ..models.order_product import OrderProduct


class LineItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderProduct
        fields = ["product", "quantity"]

    def get_product(self, obj):
        if obj.product.category_id == 2:  # If product is a pizza
            return PizzaWithToppingsSerializer(obj.product).data
        return ProductSerializer(obj.product).data
