from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from pizzaapi.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"categories", CategoryViewSet, "category")
router.register(r"lineitems", LineItemViewSet, "orderproduct")
router.register(r"payments", PaymentViewSet, "payment")
router.register(r"products", ProductViewSet, "product")
router.register(r"users", UserViewSet, "user")

urlpatterns = [
    path("", include(router.urls)),
]
