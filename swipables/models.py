from django.db import models

from common.models import TimeStampedModel


class Swipable(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(
        "restaurants.Restaurant",
        on_delete=models.CASCADE,
        related_name="swipable",
        blank=True,
        null=True,
    )
    recipe = models.ForeignKey(
        "recipes.Recipe",
        on_delete=models.CASCADE,
        related_name="swipable",
        blank=True,
        null=True,
    )

    def __str__(self):
        if self.restaurant:
            return f"{self.restaurant}"
        return f"{self.recipe}"

    class Meta:
        ordering = ["id"]
