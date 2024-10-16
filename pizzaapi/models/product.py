from django.db import models
from .category import Category


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField()
    created_date = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image_path = models.ImageField(
        upload_to="products",
        height_field=None,
        width_field=None,
        max_length=None,
        null=True,
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"
