from django.db import models
from ..models.order_product import OrderProduct
from ..models.product import Product


class PizzaTopping(models.Model):
    order_product = models.ForeignKey(
        OrderProduct,
        on_delete=models.CASCADE,
        related_name="pizza_toppings",
        limit_choices_to={"product__category": 2},  # Pizza category
        null=True,
    )
    topping = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="topping_pizzas",
        limit_choices_to={"category": 5},  # Toppings category
    )

    class Meta:
        unique_together = ["order_product", "topping"]
