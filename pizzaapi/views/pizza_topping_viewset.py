from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import PizzaTopping, Product
from ..serializers import PizzaWithToppingsSerializer


class PizzaToppingViewSet(viewsets.ModelViewSet):
    queryset = PizzaTopping.objects.all()
    serializer_class = PizzaWithToppingsSerializer

    @action(detail=True, methods=["post"])
    def add_topping(self, request, pk=None):
        pizza = self.get_object()
        topping_id = request.data.get("topping_id")

        try:
            topping = Product.objects.get(
                id=topping_id, category=5
            )  # category 5 for toppings
            PizzaTopping.objects.create(pizza=pizza, topping=topping)
            return Response(PizzaWithToppingsSerializer(pizza).data)
        except Product.DoesNotExist:
            return Response(
                {"error": "Topping not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["delete"])
    def remove_topping(self, request, pk=None):
        pizza = self.get_object()
        topping_id = request.data.get("topping_id")

        try:
            PizzaTopping.objects.filter(pizza=pizza, topping_id=topping_id).delete()
            return Response(PizzaWithToppingsSerializer(pizza).data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
