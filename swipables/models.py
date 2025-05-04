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


class Swipe(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    owner_username = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="swipes",
    )
    swipable = models.ForeignKey(
        "swipables.Swipable",
        on_delete=models.CASCADE,
        related_name="swipes",
    )
    group = models.ForeignKey(
        "groups.Group",
        on_delete=models.CASCADE,
        related_name="swipes",
    )
    score = models.IntegerField()
    session = models.IntegerField()

    def __str__(self):
        return f"{self.owner_username} - {self.swipable} - {self.group}"

    class Meta:
        ordering = ["id"]
        unique_together = ("owner_username", "swipable", "group", "session")
