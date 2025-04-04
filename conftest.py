import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.views import TokenObtainPairView

from groups.models import Group, SendGroupInvite
from recipes.models import Ingredient, Recipe


@pytest.fixture
def create_user(db):
    """
    Fixture to create a user with specific fields for testing purposes.
    """
    def make(**kwargs):
        User = get_user_model()
        return User.objects.create_user(**kwargs)

    return make


@pytest.fixture
def user(create_user):
    """
    Fixture to create a user for testing purposes.
    """
    return create_user(
        username="testuser",
        password="testpass",
        email="test@test.com"
    )


@pytest.fixture
def user2(create_user):
    """
    Fixture to create a user for testing purposes.
    """
    return create_user(
        username="testuser2",
        password="testpass",
        email="test2@test.com"
    )


@pytest.fixture
def user_tokens(user):
    """
    Fixture to obtain JWT tokens for the created user.
    """
    view = TokenObtainPairView.as_view()
    request = APIRequestFactory().post(
        "/api/token/", {
            "username": "testuser",
            "password": "testpass"
        }
    )
    response = view(request)

    if response.status_code == 200:
        return response.data
    else:
        raise Exception("Failed to obtain tokens")


@pytest.fixture
def user2_tokens(user2):
    """
    Fixture to obtain JWT tokens for the created user.
    """
    view = TokenObtainPairView.as_view()
    request = APIRequestFactory().post(
        "/api/token/", {
            "username": "testuser2",
            "password": "testpass"
        }
    )
    response = view(request)

    if response.status_code == 200:
        return response.data
    else:
        raise Exception("Failed to obtain tokens")


@pytest.fixture
def group(user):
    """
    Fixture to create a group for testing purposes.
    """
    group = Group.objects.create(name="testgroup", owner_username=user)
    group.members.add(user)
    group.save()

    return group


@pytest.fixture
def invite(user, user2, group):
    """
    Fixture to create a SendGroupInvite instance for testing purposes.
    """
    return SendGroupInvite.objects.create(
        group=group,
        sending_username=user,
        receiving_username=user2,
    )


@pytest.fixture
def ingredients(user):
    """
    Fixture to create ingredients for testing purposes.
    """
    return [
        Ingredient.objects.create(name="sugar", owner_username=user),
        Ingredient.objects.create(name="salt", owner_username=user),
        Ingredient.objects.create(name="pepper", owner_username=user),
    ]


@pytest.fixture
def recipe(user, ingredients):
    """
    Fixture to create a recipe for testing purposes.
    """
    recipe = Recipe.objects.create(
        name="pasta",
        description="Delicious pasta recipe",
        prep_time=30,
        owner_username=user,
    )
    recipe.ingredients.set(ingredients)
    recipe.steps.create(
        step_number=1, description="Boil water and cook pasta.", recipe=recipe)
    recipe.steps.create(
        step_number=2, description="Drain and serve.", recipe=recipe)
    recipe.save()

    return recipe
