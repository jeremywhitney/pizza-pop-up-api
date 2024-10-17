from rest_framework import viewsets
from ..models.order_product import OrderProduct
from ..serializers.lineitem_serializer import LineItemSerializer


class LineItemViewSet(viewsets.ModelViewSet):
    queryset = OrderProduct.objects.all()
    serializer_class = LineItemSerializer