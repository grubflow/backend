import pytest
from rest_framework.test import APIRequestFactory


from restaurants.models import Restaurant
from restaurants.views import RestaurantView

# Create your tests here.
@pytest.mark.django_db
def test_create_restaurants(admin_user_tokens):
    """Test Restaurant endpoint existence and data"""
    view = RestaurantView.as_view({"post": 'create'})
    request = APIRequestFactory().post(
        "/api/restaurants/", {
            "name": "Dairy Queen",
            "category": "Fast Food",
            
        }
    )

    token = admin_user_tokens["access"]
    request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"

    response = view(request)

    assert response.status_code == 201
    assert Restaurant.objects.filter(id = response.data["id"]).exists()
    assert response.data["name"] == "Dairy Queen"
    assert response.data["category"] == "Fast Food"