import pytest
from rest_framework.test import APIRequestFactory

from recipes.models import Step
from recipes.views import StepViewSet


@pytest.mark.django_db
def test_create_step(user_tokens, recipe):
    """
    Test creating a step
    """
    view = StepViewSet.as_view({"post": "create"})
    request = APIRequestFactory().post(
        "/api/recipes/steps/", {
            "step_number": 1,
            "description": "Prepare the pasta.",
            "recipe": recipe.pk
        },
    )
    token = user_tokens["access"]
    request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"
    response = view(request)
    recipe.refresh_from_db()

    assert response.status_code == 201
    assert response.data["description"] == "Prepare the pasta."
    step = Step.objects.get(id=response.data["id"])
    assert step.step_number == 1
    assert step.recipe == recipe
    assert recipe.steps[0].step_number == 1
    assert recipe.steps[1].step_number == 2
    assert recipe.steps[2].step_number == 3


@pytest.mark.django_db
def test_update_step(user_tokens, recipe):
    """
    Test updating a step
    """
    view = StepViewSet.as_view({"put": "update"})
    request = APIRequestFactory().put(
        f"/api/recipes/steps/{recipe.steps[0].pk}/", {
            "description": "Test change description.",
        },
    )
    token = user_tokens["access"]
    request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"
    response = view(request, pk=recipe.steps[0].pk)

    assert response.status_code == 200
    assert response.data["description"] == "Test change description."
    step = Step.objects.get(id=response.data["id"])
    assert step.description == "Test change description."


@pytest.mark.django_db
def test_delete_step(user_tokens, recipe):
    """
    Test deleting a step
    """
    recipe.steps.create(
        step_number=3,
        description="Yet another test step.",
        recipe=recipe,
    )
    recipe.save()

    assert len(recipe.steps) == 3

    pk = recipe.steps[0].pk
    view = StepViewSet.as_view({"delete": "destroy"})
    request = APIRequestFactory().delete(
        f"/api/recipes/steps/{pk}/",
    )
    token = user_tokens["access"]
    request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"
    response = view(request, pk=pk)

    assert response.status_code == 204
    assert not Step.objects.filter(pk=pk).exists()
    recipe.refresh_from_db()
    assert recipe.steps[0].step_number == 1
    assert recipe.steps[1].step_number == 2
