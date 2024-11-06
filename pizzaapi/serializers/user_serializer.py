from rest_framework import serializers
from django.contrib.auth.models import User
from ..models.profile import Profile
from ..models.employee_profile import EmployeeProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "date_joined",
        ]


class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.CharField(source="user.email")
    is_staff = serializers.BooleanField(source="user.is_staff", read_only=True)
    position = serializers.CharField(source="employeeprofile.position", read_only=True)
    rate = serializers.FloatField(source="employeeprofile.rate", read_only=True)
    date_joined = serializers.DateTimeField(source="user.date_joined", format="%m-%d-%Y", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "phone_number",
            "address",
            "position",
            "rate",
            "date_joined",
        ]

    def to_representation(self, instance):
        """Customize the output based on user type"""
        ret = super().to_representation(instance)

        if not instance.user.is_staff:
            # Remove employee-specific fields for non-staff users
            ret.pop("position", None)
            ret.pop("rate", None)
            ret.pop("date_joined", None)

        return ret


class EmployeeProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeeProfile
        fields = ["position", "rate"]


class EmployeeOrderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="user.id")
    username = serializers.CharField(source="user.username")

    class Meta:
        model = Profile
        fields = ["id", "username"]
