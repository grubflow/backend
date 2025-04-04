from rest_framework.routers import DefaultRouter

from restaurants.views import RestaurantView

router = DefaultRouter()
router.register('', RestaurantView, basename='user')

urlpatterns = router.urls
