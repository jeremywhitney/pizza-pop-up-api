from rest_framework import serializers
from .lineitem_serializer import LineItemSerializer
from .user_serializer import ProfileSerializer, EmployeeOrderSerializer
from .payment_serializer import OrderPaymentSerializer
from ..models import Order, OrderProduct, PizzaTopping


class OrderSerializer(serializers.ModelSerializer):
    customer = ProfileSerializer(read_only=True)
    employee = EmployeeOrderSerializer(read_only=True)
    payment = OrderPaymentSerializer(read_only=True)
    products = LineItemSerializer(source="orderproduct_set", many=True)
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

    def create(self, validated_data):
        # Extract the original 'products' data from the initial request data
        products_data = self.initial_data.get("products")

        # Get the request object to access the user for the customer field
        request = self.context.get("request")
        validated_data["customer"] = request.user.profile

        # Remove any nested fields from 'validated_data' that belong to other models
        if "orderproduct_set" in validated_data:
            validated_data.pop("orderproduct_set")  # Remove if present

        # Create the Order instance (no nested fields)
        order = Order.objects.create(**validated_data)

        # Loop through each product in 'products_data' to create OrderProduct and PizzaTopping
        for product_data in products_data:
            # Extract the product ID and quantity
            product_id = product_data.pop("product")
            quantity = product_data.pop("quantity")

            # Create the OrderProduct instance
            order_product = OrderProduct.objects.create(
                order=order, product_id=product_id, quantity=quantity
            )

            # Handle pizza toppings if provided
            toppings_data = product_data.get("toppings", [])
            for topping in toppings_data:
                PizzaTopping.objects.create(
                    order_product=order_product, topping_id=topping["id"]
                )

        # Return the created order with nested products and toppings handled
        return order
