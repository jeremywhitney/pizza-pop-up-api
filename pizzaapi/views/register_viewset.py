from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import EmployeeProfile
from ..serializers.user_serializer import (
    UserSerializer,
    ProfileSerializer,
    EmployeeProfileSerializer,
)


class RegisterViewSet(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        profile_serializer = ProfileSerializer(data=request.data)

        # Check if both user and profile data are valid
        if user_serializer.is_valid() and profile_serializer.is_valid():
            user = user_serializer.save(
                is_staff=False
            )  # Set is_staff to False by default

            # Hash the password using set_password
            user.set_password(request.data["password"])
            user.save()

            # Create profile using the serializer
            profile = profile_serializer.save(user=user)

            # Handle employee registration
            if "employee_profile" in request.data:
                employee_serializer = EmployeeProfileSerializer(
                    data=request.data["employee_profile"]
                )
                if employee_serializer.is_valid():
                    # Create employee profile and set user as staff
                    EmployeeProfile.objects.create(
                        profile=profile, **employee_serializer.validated_data
                    )
                    user.is_staff = True
                    user.save()
                else:
                    # If employee serializer isn't valid, return error
                    return Response(
                        employee_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

            token = Token.objects.create(user=user)
            return Response(
                {"token": token.key, "user_id": user.id, "is_staff": user.is_staff},
                status=status.HTTP_201_CREATED,
            )

        # If validation fails, return all errors
        errors = {}
        if not user_serializer.is_valid():
            errors.update(user_serializer.errors)
        if not profile_serializer.is_valid():
            errors.update(profile_serializer.errors)

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
