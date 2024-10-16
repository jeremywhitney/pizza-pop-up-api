from django.db import models
from .profile import Profile


class EmployeeProfile(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    position = models.CharField(max_length=255)
    rate = models.FloatField()

    def __str__(self):
        return str(f"{self.profile.user.username} - {self.position}")

    class Meta:
        verbose_name = "employee profile"
        verbose_name_plural = "employee profiles"
