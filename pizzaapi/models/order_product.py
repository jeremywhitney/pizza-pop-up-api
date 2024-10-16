from django.db import models
from .order import Order
from .product import Product


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(f"{self.order.id} - {self.product.name} (x{self.quantity})")

    class Meta:
        verbose_name = "order product"
        verbose_name_plural = "order products"
