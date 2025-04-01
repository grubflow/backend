import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.views import TokenObtainPairView

from users.views import UserViewset


@pytest.mark.django_db
def test_create_user():
    """Test user registration endpoint"""
    view = UserViewset.as_view({"post": 'create'})
    request = APIRequestFactory().post(
        "/api/users/", {
            "username": "testuser",
            "password": "testpass8884",
            "email": "test@test.com"
        }
    )
    response = view(request)

    assert response.status_code == 201
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_login(user):
    """Test login endpoint"""
    view = TokenObtainPairView.as_view()
    request = APIRequestFactory().post(
        "/api/token/", {
            "username": "testuser",
            "password": "testpass"
        }
    )
    response = view(request)

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_user_detail(user_tokens):
    """Test user detail endpoint"""
    view = UserViewset.as_view({"get": "current"})
    request = APIRequestFactory().get("/api/users/current/")
    token = user_tokens["access"]
    request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"
    response = view(request)

    assert response.status_code == 200
    assert response.data["username"] == "testuser"
    assert response.data["email"] == "test@test.com"


@pytest.mark.django_db
def test_user_update(user, user_tokens):
    """Test user update endpoint"""
    assert user.email == "test@test.com"
    initial_password = user.password

    view = UserViewset.as_view({"patch": "partial_update"})
    request = APIRequestFactory().patch(
        "/api/users/testuser/", {
            "email": "test2@test.com",
            "password": "39338testhello!"
        }
    )
    token = user_tokens["access"]
    request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"
    response = view(request, pk=user.username)
    user = get_user_model().objects.get(username="testuser")

    assert response.status_code == 200
    assert response.data["email"] == "test2@test.com"
    assert user.password != initial_password
