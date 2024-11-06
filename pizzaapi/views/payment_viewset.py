from rest_framework import viewsets
from ..models.payment import Payment
from ..serializers.payment_serializer import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        user = self.request.user
        # Superusers and staff can see all payment methods
        if user.is_superuser or user.is_staff:
            return Payment.objects.all()
        # Regular users only see their payment methods
        return Payment.objects.filter(customer__user=user)
