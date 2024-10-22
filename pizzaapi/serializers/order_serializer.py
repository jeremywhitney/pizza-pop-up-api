from rest_framework import serializers
from .lineitem_serializer import LineItemSerializer
from .user_serializer import ProfileSerializer, EmployeeOrderSerializer
from .payment_serializer import OrderPaymentSerializer
from ..models import Order, OrderProduct, PizzaTopping


class OrderSerializer(serializers.ModelSerializer):
    customer = ProfileSerializer(read_only=True)
    employee = EmployeeOrderSerializer(read_only=True)
    payment = OrderPaymentSerializer(read_only=True)
    products = LineItemSerializer(many=True, source="orderproduct_set")
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
        products_data = self.initial_data.get("products")
        request = self.context.get("request")
        validated_data["customer"] = request.user.profile

        # Remove the nested orderproduct_set from validated_data if present
        validated_data.pop("orderproduct_set", None)

        # Create the order instance
        order = Order.objects.create(**validated_data)

        # Process each product in products_data
        for product_data in products_data:
            product_id = product_data.pop("id")  # Using id field for product
            quantity = product_data.pop("quantity")

            # Create the OrderProduct
            order_product = OrderProduct.objects.create(
                order=order, product_id=product_id, quantity=quantity
            )

            # Create any pizza toppings for this order product
            toppings_data = product_data.get("toppings", [])
            for topping in toppings_data:
                PizzaTopping.objects.create(
                    order_product=order_product, topping_id=topping["id"]
                )

        return order

    def update(self, instance, validated_data):
        # Handle status and other top-level fields
        instance.status = validated_data.get("status", instance.status)

        # Handle payment updates
        payment_data = self.initial_data.get("payment")
        if payment_data:
            payment_id = payment_data.get("id")
            instance.payment_id = payment_id  # Update payment relationship

        # Handle employee updates
        employee_data = self.initial_data.get("employee")
        if employee_data:
            employee_id = employee_data.get("id")
            instance.employee_id = employee_id  # Update employee relationship

        # Handle product updates (order products)
        products_data = self.initial_data.get("products")
        if products_data:
            # Clear out existing order products
            instance.orderproduct_set.all().delete()

            for product_data in products_data:
                product_id = product_data.pop("id")
                quantity = product_data.pop("quantity")

                order_product = OrderProduct.objects.create(
                    order=instance, product_id=product_id, quantity=quantity
                )

                # Handle pizza toppings updates (if applicable)
                toppings_data = product_data.get("toppings", [])
                for topping in toppings_data:
                    PizzaTopping.objects.create(
                        order_product=order_product, topping_id=topping["id"]
                    )

        # Save the order instance with updated fields
        instance.save()

        return instance
