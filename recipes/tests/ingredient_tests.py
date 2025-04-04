import pytest
from rest_framework.test import APIRequestFactory

from recipes.models import Ingredient
from recipes.views import IngredientViewSet


@pytest.mark.django_db
def test_create_ingredient(user, user_tokens):
    """
    Test creating an ingredient
    """
    view = IngredientViewSet.as_view({"post": "create"})
    request = APIRequestFactory().post(
        "/api/recipes/ingredients/", {
            "name": "sugar",
        }
    )
    token = user_tokens["access"]
    request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"
    response = view(request)
    ingredient = Ingredient.objects.get(name="sugar")

    assert response.status_code == 201
    assert response.data["name"] == "sugar"
    assert ingredient.owner_username == user
