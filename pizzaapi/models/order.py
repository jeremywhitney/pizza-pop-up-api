from django.db import models
from .profile import Profile
from .payment import Payment
from .product import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("IN_PROCESS", "In Process"),
        ("COMPLETED", "Completed"),
    ]

    customer = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="customer_orders"
    )
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, null=True, blank=True
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    created_date = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, through="OrderProduct")
    employee = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employee_orders",
    )

    def __str__(self):
        return str(
            f"Order {self.id} - {self.customer.user.username} - {self.get_status_display()}"
        )

    class Meta:
        verbose_name = "order"
        verbose_name_plural = "orders"

    def is_cart(self):
        return self.payment is None and self.status == "PENDING"

    def total_price(self):
        return sum(op.product.price * op.quantity for op in self.orderproduct_set.all())
