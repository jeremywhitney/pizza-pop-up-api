from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from ..models import EmployeeProfile
from ..serializers.user_serializer import (
    UserSerializer,
    ProfileSerializer,
    EmployeeProfileSerializer,
)


class RegisterViewSet(APIView):
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        profile_serializer = ProfileSerializer(data=request.data)

        if user_serializer.is_valid() and profile_serializer.is_valid():
            user = user_serializer.save()
            profile = profile_serializer.save(user=user)

            is_employee = request.data.get("is_employee", False)
            if is_employee:
                employee_serializer = EmployeeProfileSerializer(data=request.data)
                if employee_serializer.is_valid():
                    EmployeeProfile.objects.create(
                        profile=profile, **employee_serializer.validated_data
                    )
                    user.is_staff = True
                    user.save()
                else:
                    return Response(
                        employee_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

            token = Token.objects.create(user=user)
            return Response(
                {"token": token.key, "user_id": user.id, "is_staff": user.is_staff},
                status=status.HTTP_201_CREATED,
            )

        errors = {}
        errors.update(user_serializer.errors)
        errors.update(profile_serializer.errors)
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
