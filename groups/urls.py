from rest_framework import routers

from groups.views import GroupViewset

router = routers.DefaultRouter()
router.register('', GroupViewset, basename='group')

urlpatterns = router.urls
