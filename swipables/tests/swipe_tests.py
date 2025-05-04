import pytest
from rest_framework.test import APIRequestFactory

from groups.views import GroupViewset
from swipables.models import Swipable
from swipables.views import SwipeViewset


@pytest.mark.django_db
def test_swiping(user, user_tokens, group, recipe):
    """
    Test creating a swipe from a swipable
    """
    swipable_id = Swipable.objects.filter(
        recipe=recipe
    ).first().pk
    view = SwipeViewset.as_view({"post": "create"})
    request = APIRequestFactory().post(
        "/api/swipes/", {
            "group": group.pk,
            "swipable": swipable_id,
            "score": 100,
        }
    )
    token = user_tokens["access"]
    request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"
    response = view(request)

    print(response.data)

    assert response.status_code == 201
    assert response.data["owner_username"] == user.username
    assert response.data["session"] == group.num_sessions

    view = GroupViewset.as_view({"get": "scores"})
    request = APIRequestFactory().get(f"/api/groups/{group.pk}/scores/")
    request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"
    response = view(request, pk=group.pk)

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["swipable"]["id"] == swipable_id
