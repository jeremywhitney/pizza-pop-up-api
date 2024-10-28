from rest_framework import serializers
from .user_serializer import ProfileSerializer
from ..models.payment import Payment


class PaymentSerializer(serializers.ModelSerializer):
    customer = ProfileSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "merchant_name",
            "account_number",
            "customer",
            "expiration_date",
            "create_date",
        ]
        read_only_fields = ["id", "create_date"]

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["customer"] = request.user.profile
        return super().create(validated_data)


class OrderPaymentSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = [
            "id",
            "merchant_name",
            "account_number",
            "customer",
            "expiration_date",
        ]

    def get_customer(self, obj):
        return {"id": obj.customer.user.id, "username": obj.customer.user.username}
