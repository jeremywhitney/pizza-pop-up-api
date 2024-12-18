from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from pizzaapi.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"categories", CategoryViewSet, "category")
router.register(r"lineitems", LineItemViewSet, "orderproduct")
router.register(r"orders", OrderViewSet, "order")
router.register(r"payments", PaymentViewSet, "payment")
router.register(r"pizza_toppings", PizzaToppingViewSet, "pizzatopping")
router.register(r"products", ProductViewSet, "product")
router.register(r"users", UserViewSet, "user")

urlpatterns = [
    path("", include(router.urls)),
    path("login", LoginViewSet.as_view(), name="login"),
    path("register", RegisterViewSet.as_view(), name="register"),
    path(
        "profile/",
        UserViewSet.as_view({"get": "profile", "patch": "update_profile"}),
        name="profile",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
