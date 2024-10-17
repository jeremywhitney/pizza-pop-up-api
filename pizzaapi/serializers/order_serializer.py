from rest_framework import serializers
from ..models.order import Order
from .order_product_serializer import OrderProductSerializer
from .user_serializer import ProfileSerializer
from .payment_serializer import PaymentSerializer


class OrderSerializer(serializers.ModelSerializer):
    customer = ProfileSerializer(read_only=True)
    employee = ProfileSerializer(read_only=True)
    payment = PaymentSerializer(read_only=True)
    products = OrderProductSerializer(source="orderproduct_set", many=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "customer",
            "status",
            "created_date",
            "products",
            "employee",
            "payment",
            "total_price",
        ]

    def get_total_price(self, obj):
        """Method to calculate the total price of the order"""
        return obj.total_price()
