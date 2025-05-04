import pytest
from rest_framework.test import APIRequestFactory

from swipables.models import Swipe
from swipables.views import SwipableListView


@pytest.mark.django_db
def test_filter_swipables(user, user_tokens, group, recipe, restaurant):
    """
    Test excluding swipables that have been swiped
    """
    view = SwipableListView.as_view()
    request = APIRequestFactory().get(
        f"/api/swipables/?group={group.pk}"
    )
    token = user_tokens["access"]
    request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"
    response = view(request)

    assert response.status_code == 200
    assert response.data["count"] == 2

    Swipe.objects.create(
        owner_username=user,
        swipable_id=response.data["results"][0]["id"],
        group=group,
        score=100,
        session=group.num_sessions
    )

    response = view(request)
    assert response.status_code == 200
    assert response.data["count"] == 1
