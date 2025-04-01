import pytest
from rest_framework.test import APIRequestFactory

from groups.models import Group
from groups.views import SendGroupInviteViewset


@pytest.mark.django_db
def test_invite_create(user, user_tokens, user2, group):
    """
    Test creating a group invite
    """
    view = SendGroupInviteViewset.as_view({"post": "create"})
    request = APIRequestFactory().post(
        "/api/groups/invite/", {
            "group": group.composite_key,
            "receiving_username": user2.username
        }
    )
    token = user_tokens["access"]
    request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"
    response = view(request)

    assert response.status_code == 201
    assert response.data["group"] == group.composite_key
    assert response.data["receiving_username"] == user2.username
    assert response.data["sending_username"] == user.username


@pytest.mark.django_db
def test_invite_accept(user2, user2_tokens, invite):
    """
    Test accepting an invite
    """
    view = SendGroupInviteViewset.as_view({"put": "update"})
    request = APIRequestFactory().put(
        f"/api/groups/invite/{invite.composite_key}/", {
            "accepted": True
        }
    )
    token = user2_tokens["access"]
    request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"
    response = view(request, pk=invite.composite_key)
    group = Group.objects.get(composite_key=invite.group.composite_key)

    assert response.status_code == 200
    assert response.data["accepted"] is True
    assert user2 in group.members.all()


@pytest.mark.django_db
def test_invite_decline(user2, user2_tokens, invite):
    """
    Test declining an invite
    """
    view = SendGroupInviteViewset.as_view({"put": "update"})
    request = APIRequestFactory().put(
        f"/api/groups/invite/{invite.composite_key}/", {
            "accepted": False
        }
    )
    token = user2_tokens["access"]
    request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"
    response = view(request, pk=invite.composite_key)
    group = Group.objects.get(composite_key=invite.group.composite_key)

    assert response.status_code == 200
    assert response.data["accepted"] is False
    assert user2 not in group.members.all()


@pytest.mark.django_db
def test_group_full(create_user, user2, user2_tokens, invite):
    """
    Test accepting an invite when the group is full
    """
    group = invite.group
    for i in range(3, group.capacity + 2):
        user = create_user(
            username=f"test{i}",
            password="testpass",
            email=f"test{i}@test.com"
        )
        group.members.add(user)
    group.save()

    assert group.member_count == group.capacity

    view = SendGroupInviteViewset.as_view({"put": "update"})
    request = APIRequestFactory().put(
        f"/api/groups/invite/{invite.composite_key}/", {
            "accepted": True
        }
    )
    token = user2_tokens["access"]
    request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"
    response = view(request, pk=invite.composite_key)
    group = Group.objects.get(composite_key=invite.group.composite_key)

    assert response.status_code == 400
    assert user2 not in group.members.all()
