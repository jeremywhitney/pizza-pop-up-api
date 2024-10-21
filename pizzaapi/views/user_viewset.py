from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from ..serializers import *
from ..models import Profile, EmployeeProfile, Order, Payment


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Override retrieve to include employee data for staff users
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Fetch customer profile
        try:
            profile = Profile.objects.get(user=instance)
            profile_serializer = ProfileSerializer(profile)
            profile_data = profile_serializer.data
        except Profile.DoesNotExist:
            profile_data = None

        # If user is staff, fetch employee profile and add it to the profile data
        if instance.is_staff and profile_data:
            try:
                employee_profile = EmployeeProfile.objects.get(profile=profile)
                employee_serializer = EmployeeProfileSerializer(employee_profile)
                # Add employee fields to profile data
                profile_data.update(employee_serializer.data)
            except EmployeeProfile.DoesNotExist:
                pass

        # Combine data into a custom response
        return Response(
            {
                "profile": profile_data if profile_data else None,
            }
        )

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
