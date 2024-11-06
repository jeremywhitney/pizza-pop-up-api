from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
