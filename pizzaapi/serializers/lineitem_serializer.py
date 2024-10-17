from rest_framework import serializers
from .product_serializer import ProductSerializer
from ..models.order_product import OrderProduct


class LineItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderProduct
        fields = ["product", "quantity"]
