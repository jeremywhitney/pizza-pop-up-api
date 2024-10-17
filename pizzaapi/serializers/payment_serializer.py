from rest_framework import serializers
from .user_serializer import ProfileSerializer
from ..models.payment import Payment


class PaymentSerializer(serializers.ModelSerializer):
    customer = ProfileSerializer()

    class Meta:
        model = Payment
        fields = [
            "merchant_name",
            "account_number",
            "customer",
            "expiration_date",
            "create_date",
        ]
