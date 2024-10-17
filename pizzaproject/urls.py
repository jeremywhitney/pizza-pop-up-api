from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from pizzaapi.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"categories", CategoryViewSet, "category")
router.register(r"payments", PaymentViewSet, "payment")

urlpatterns = [
    path("", include(router.urls)),
]
