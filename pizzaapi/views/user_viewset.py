from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User
from ..serializers.user_serializer import (
    UserSerializer,
    ProfileSerializer,
    EmployeeProfileSerializer,
)
from ..models.profile import Profile
from ..models.employee_profile import EmployeeProfile


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Override retrieve to include employee data for staff users
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user_serializer = UserSerializer(instance)

        # Fetch customer profile
        try:
            profile = Profile.objects.get(user=instance)
            profile_serializer = ProfileSerializer(profile)
        except Profile.DoesNotExist:
            profile_serializer = None

        # Fetch employee profile if the user is staff
        if instance.is_staff:
            try:
                employee_profile = EmployeeProfile.objects.get(profile=profile)
                employee_serializer = EmployeeProfileSerializer(employee_profile)
            except EmployeeProfile.DoesNotExist:
                employee_serializer = None
        else:
            employee_serializer = None

        # Combine data into a custom response
        return Response(
            {
                "user": user_serializer.data,
                "profile": profile_serializer.data if profile_serializer else None,
                "employee_profile": (
                    employee_serializer.data if employee_serializer else None
                ),
            }
        )
