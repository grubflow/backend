from django.test import TestCase
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.views import TokenObtainPairView

from restaurants.models import Restaurant
from restaurants.views import RestaurantView

# Create your tests here.
@pytest.mark.django_db
def test_create_restaurants(user_tokens):
    """Test user registration endpoint"""
    view = RestaurantView.as_view({"post": 'create'})
    request = APIRequestFactory().post(
        "/api/restaurants/", {
            "name": "Dairy Queen",
            "category": "Fast Food",
            
        }
    )

    token = user_tokens["access"]
    request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"

    response = view(request)

    assert response.status_code == 201
    assert Restaurant.objects.filter(id = response.data["id"]).exists()
    assert response.data["name"] == "Dairy Queen"
    assert response.data["category"] == "Fast Food"