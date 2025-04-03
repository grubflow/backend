from django.db import models

from common.models import TimeStampedModel


class Recipe(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    description = models.TextField(max_length=1000)
    prep_time = models.IntegerField()
    owner_username = models.ForeignKey(
        'users.User', related_name='recipe_set', on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(
        'recipes.Ingredient', related_name='recipe_set')

    @property
    def steps(self):
        return self.step_set.all()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        unique_together = ('name', 'owner_username')


class Step(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    recipe = models.ForeignKey(
        'recipes.Recipe', related_name='step_set', on_delete=models.CASCADE)
    step_number = models.IntegerField()
    description = models.TextField(max_length=1000)

    def __str__(self):
        return f"Step {self.step_number} of {self.recipe.name}"


class Ingredient(TimeStampedModel):
    name = models.CharField(max_length=255, primary_key=True)
    owner_username = models.ForeignKey(
        'users.User', related_name='ingredient_set', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
