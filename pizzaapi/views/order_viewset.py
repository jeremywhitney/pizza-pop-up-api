from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models.order import Order
from ..serializers.order_serializer import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # Override get_queryset to filter by cart or orders
    def get_queryset(self):
        user = self.request.user
        # Superusers and staff can see all orders
        if user.is_superuser or user.is_staff:
            return Order.objects.all()
        # Regular users only see their orders
        return Order.objects.filter(customer__user=user)

    def update(self, request, *args, **kwargs):
        order = self.get_object()

        # If status is being changed
        if "status" in request.data:
            if not request.user.is_staff:
                return Response(
                    {"error": "Only staff can update order status"}, status=403
                )

            new_status = request.data["status"]
            current_status = order.status

            # Validate status transitions
            if current_status == "PENDING" and new_status != "IN_PROCESS":
                return Response(
                    {"error": "Pending orders can only be changed to In Process"},
                    status=400,
                )
            elif current_status == "IN_PROCESS" and new_status != "COMPLETED":
                return Response(
                    {"error": "In Process orders can only be changed to Completed"},
                    status=400,
                )
            elif current_status == "COMPLETED":
                return Response(
                    {"error": "Completed orders cannot be changed"}, status=400
                )

            # If changing to IN_PROCESS, set the employee
            if new_status == "IN_PROCESS":
                order.employee = request.user.profile
                order.save()

        return super().update(request, *args, **kwargs)

    # Action to fetch completed orders (those with payments and a status)
    @action(detail=False, methods=["get"], url_path="completed")
    def get_completed_orders(self, request):
        user = request.user
        completed_orders = Order.objects.filter(
            customer__user=user,
            payment__isnull=False,
            status__in=["IN_PROCESS", "In Process", "COMPLETED", "Completed"],
        )
        serializer = self.get_serializer(completed_orders, many=True)
        return Response(serializer.data)
