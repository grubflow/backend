import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.views import TokenObtainPairView

from groups.models import Group, SendGroupInvite


@pytest.fixture
def user(db):
    """
    Fixture to create a user for testing purposes.
    """
    User = get_user_model()
    return User.objects.create_user(
        username="testuser",
        password="testpass",
        email="test@test.com"
    )


@pytest.fixture
def user2(db):
    """
    Fixture to create a user for testing purposes.
    """
    User = get_user_model()
    return User.objects.create_user(
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
def group(db, user):
    """
    Fixture to create a group for testing purposes.
    """
    group = Group.objects.create(name="testgroup", owner_username=user)
    group.members.add(user)
    group.save()

    return group


@pytest.fixture
def invite(db, user, user2, group):
    """
    Fixture to create a SendGroupInvite instance for testing purposes.
    """
    return SendGroupInvite.objects.create(
        group=group,
        sending_username=user,
        receiving_username=user2,
    )
