from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return str(f"{self.user.username}'s profile")

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"
