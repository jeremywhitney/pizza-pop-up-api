from django.db import models
from .product import Product


class PizzaTopping(models.Model):
    pizza = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="pizza_toppings",
        limit_choices_to={"category": 2},  # Pizza category
    )
    topping = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="topping_pizzas",
        limit_choices_to={"category": 5},  # Toppings category
    )

    class Meta:
        unique_together = ["pizza", "topping"]
