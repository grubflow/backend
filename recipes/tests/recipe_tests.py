import pytest
from rest_framework.test import APIRequestFactory

from recipes.models import Recipe
from recipes.views import RecipeViewSet


@pytest.mark.django_db
def test_create_recipe(user, user_tokens, ingredients):
    """
    Test creating a recipe
    """
    view = RecipeViewSet.as_view({"post": "create"})
    request = APIRequestFactory().post(
        "/api/recipes/", {
            "name": "Pasta",
            "description": "Delicious pasta recipe",
            "prep_time": 30,
            "ingredients": ["sugar"],
            "steps": [
                {
                    "description": "Boil water and cook pasta."
                },
                {
                    "description": "Drain and serve."
                }
            ]
        },
        format="json"
    )
    token = user_tokens["access"]
    request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"
    response = view(request)

    assert response.status_code == 201
    assert response.data["name"] == "pasta"
    assert response.data["ingredients"] == ["sugar"]
    recipe = Recipe.objects.get(name="pasta", owner_username=user)
    assert len(recipe.steps) == 2


@pytest.mark.django_db
def test_get_recipe(user_tokens, recipe):
    """
    Test getting a recipe
    """
    view = RecipeViewSet.as_view({"get": "retrieve"})
    request = APIRequestFactory().get(
        f"/api/recipes/{recipe.pk}/"
    )
    token = user_tokens["access"]
    request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"
    response = view(request, pk=recipe.pk)

    assert response.status_code == 200
    assert response.data["name"] == "pasta"
    assert response.data["description"] == "Delicious pasta recipe"
    assert response.data["prep_time"] == 30
    assert len(response.data["ingredients"]) == 3
    assert len(response.data["steps"]) == 2


@pytest.mark.django_db
def test_update_recipe(user_tokens, recipe):
    """
    Test updating a recipe
    """
    view = RecipeViewSet.as_view({"put": "update"})
    request = APIRequestFactory().put(
        f"/api/recipes/{recipe.pk}/", {
            "name": "Pasta",
            "description": "Updated description",
            "prep_time": 25,
            "ingredients": ["sugar", "salt"],
        },
        format="json"
    )
    token = user_tokens["access"]
    request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"
    response = view(request, pk=recipe.pk)

    assert response.status_code == 200
    assert response.data["description"] == "Updated description"
    assert len(response.data["ingredients"]) == 2


@pytest.mark.django_db
def test_delete_recipe(user_tokens, recipe):
    """
    Test deleting a recipe
    """
    view = RecipeViewSet.as_view({"delete": "destroy"})
    request = APIRequestFactory().delete(
        f"/api/recipes/{recipe.pk}/"
    )
    token = user_tokens["access"]
    request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"
    response = view(request, pk=recipe.pk)

    assert response.status_code == 204
    assert Recipe.objects.filter(pk=recipe.pk).count() == 0
