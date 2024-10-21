from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models.order import Order
# from ..permissions.order_permissions import OrderPermission
from ..serializers.order_serializer import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # permission_classes = [OrderPermission]

    # Override get_queryset to filter by cart or orders
    def get_queryset(self):
        user = self.request.user
        # Superusers and staff can see all orders
        if user.is_superuser or user.is_staff:
            return Order.objects.all()
        # Regular users only see their orders
        return Order.objects.filter(customer__user=user)

    # Action to fetch cart items only (PENDING orders with no payment)
    @action(detail=False, methods=["get"], url_path="cart")
    def get_cart(self, request):
        user = request.user
        cart = Order.objects.filter(customer__user=user, payment=None, status="PENDING")
        serializer = self.get_serializer(cart, many=True)
        return Response(serializer.data)

    # Action to fetch completed orders (those with payments and a status)
    @action(detail=False, methods=["get"], url_path="completed")
    def get_completed_orders(self, request):
        user = request.user
        completed_orders = Order.objects.filter(
            customer__user=user,
            payment__isnull=False,
            status__in=["IN_PROCESS", "COMPLETED"],
        )
        serializer = self.get_serializer(completed_orders, many=True)
        return Response(serializer.data)
