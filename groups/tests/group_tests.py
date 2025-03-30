import pytest
from rest_framework.test import APIRequestFactory

from groups.models import Group
from groups.views import GroupViewset


@pytest.mark.django_db
def test_create_group(user, user_tokens):
    """
    Test creating a group
    """
    view = GroupViewset.as_view({"post": "create"})
    request = APIRequestFactory().post(
        "/api/groups/", {
            "name": "testgroup"
        }
    )
    token = user_tokens["access"]
    request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"
    response = view(request)

    assert response.status_code == 201
    assert response.data["name"] == "testgroup"
    assert response.data["owner_username"] == user.username
    assert response.data["member_count"] == 1


@pytest.mark.django_db
def test_group_detail(user, user_tokens, group):
    """
    Test retrieving group details
    """
    view = GroupViewset.as_view({"get": "retrieve"})
    request = APIRequestFactory().get(f"/api/groups/{group.composite_key}/")
    token = user_tokens["access"]
    request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"
    response = view(request, pk=group.composite_key)

    assert response.status_code == 200
    assert response.data["name"] == group.name
    assert response.data["owner_username"] == user.username
    assert response.data["member_count"] == 1


@pytest.mark.django_db
def test_group_delete(user_tokens, group):
    """
    Test deleting a group
    """
    view = GroupViewset.as_view({"delete": "destroy"})
    request = APIRequestFactory().delete(f"/api/groups/{group.composite_key}/")
    token = user_tokens["access"]
    request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"
    response = view(request, pk=group.composite_key)

    assert response.status_code == 204
    assert not Group.objects.filter(composite_key=group.composite_key).exists()


@pytest.mark.django_db
def test_leave_group(user2, user2_tokens, group):
    """
    Test leaving a group
    """
    group.members.add(user2)
    group.save()

    assert user2 in group.members.all()

    view = GroupViewset.as_view({"delete": "leave"})
    request = APIRequestFactory().delete(
        f"/api/groups/{group.composite_key}/leave/")
    token = user2_tokens["access"]
    request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"
    response = view(request, pk=group.composite_key)
    group.refresh_from_db()

    assert response.status_code == 204
    assert user2 not in group.members.all()
