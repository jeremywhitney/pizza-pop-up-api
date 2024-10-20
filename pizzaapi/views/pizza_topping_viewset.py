from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import PizzaTopping, Product
from ..serializers import PizzaToppingSerializer


class PizzaToppingViewSet(viewsets.ModelViewSet):
    queryset = PizzaTopping.objects.all()
    serializer_class = PizzaToppingSerializer

    @action(detail=True, methods=["post"])
    def add_topping(self, request, pk=None):
        order_product = self.get_object()
        topping_id = request.data.get("topping_id")

        try:
            # Ensure the topping belongs to category 5 (Toppings)
            topping = Product.objects.get(id=topping_id, category=5)
            PizzaTopping.objects.create(order_product=order_product, topping=topping)
            return Response(PizzaToppingSerializer(order_product).data)
        except Product.DoesNotExist:
            return Response(
                {"error": "Topping not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["delete"])
    def remove_topping(self, request, pk=None):
        order_product = self.get_object()
        topping_id = request.data.get("topping_id")

        try:
            PizzaTopping.objects.filter(
                order_product=order_product, topping_id=topping_id
            ).delete()
            return Response(PizzaToppingSerializer(order_product).data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
