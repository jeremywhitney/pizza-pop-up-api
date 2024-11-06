from django.db import models
from .profile import Profile


class Payment(models.Model):
    merchant_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=255)
    customer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    expiration_date = models.DateField()
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(f"{self.merchant_name} - {self.customer.user.username}")

    class Meta:
        verbose_name = "payment"
        verbose_name_plural = "payments"
