from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from ..serializers import *
from ..models import Profile, EmployeeProfile, Order, Payment


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_profile_data(self, user):
        # Fetch customer profile
        try:
            profile = Profile.objects.get(user=user)
            profile_serializer = ProfileSerializer(profile)
            profile_data = profile_serializer.data
        except Profile.DoesNotExist:
            profile_data = None

        # If the user is staff, fetch the employee profile
        if user.is_staff and profile_data:
            try:
                employee_profile = EmployeeProfile.objects.get(profile=profile)
                employee_serializer = EmployeeProfileSerializer(employee_profile)
                # Add employee fields to the profile data
                profile_data.update(employee_serializer.data)
            except EmployeeProfile.DoesNotExist:
                pass

        return profile_data

    # Override retrieve to use the helper method
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        profile_data = self.get_profile_data(instance)
        return Response({"profile": profile_data})

    @action(detail=False, methods=["get"], url_path="profile")
    def profile(self, request):
        # Get the logged-in user
        instance = request.user

        # Fetch profile, payment methods, and orders
        profile = Profile.objects.get(user=instance)
        payments = Payment.objects.filter(customer=profile)
        orders = Order.objects.filter(customer=profile)

        profile_serializer = ProfileSerializer(profile)
        payments_serializer = PaymentSerializer(payments, many=True)
        orders_serializer = OrderSerializer(orders, many=True)

        return Response(
            {
                "profile": profile_serializer.data,
                "payments": payments_serializer.data,
                "orders": orders_serializer.data,
            }
        )

    @action(detail=False, methods=["patch"], url_path="profile")
    def update_profile(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)

        # Separate user and profile fields
        user_fields = ["username", "first_name", "last_name", "email"]
        profile_fields = ["phone_number", "address"]

        # Update User model fields
        user_data = {
            key: request.data[key] for key in user_fields if key in request.data
        }
        if user_data:
            user_serializer = UserSerializer(user, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
            else:
                return Response(user_serializer.errors, status=400)

        # Update Profile model fields
        profile_data = {
            key: request.data[key] for key in profile_fields if key in request.data
        }
        if profile_data:
            profile_serializer = ProfileSerializer(
                profile, data=profile_data, partial=True
            )
            if profile_serializer.is_valid():
                profile_serializer.save()
            else:
                return Response(profile_serializer.errors, status=400)

        # Return updated profile data
        return self.profile(request)
