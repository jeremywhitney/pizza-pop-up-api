from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .user_viewset import UserViewSet


class LoginViewSet(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            profile_data = UserViewSet().get_profile_data(user)

            return Response({"token": token.key, "profile": profile_data})

        return Response(
            {"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
        )
