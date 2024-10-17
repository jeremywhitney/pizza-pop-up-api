from rest_framework import viewsets
from ..models.payment import Payment
from ..serializers.payment_serializer import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
