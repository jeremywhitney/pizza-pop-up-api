from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ..models.product import Product
from ..serializers.product_serializer import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
