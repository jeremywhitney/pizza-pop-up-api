from rest_framework import serializers
from django.contrib.auth.models import User
from ..models.profile import Profile
from ..models.employee_profile import EmployeeProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "is_staff"]


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ["user", "phone_number", "address"]


class EmployeeProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = EmployeeProfile
        fields = ["profile", "position", "rate"]
