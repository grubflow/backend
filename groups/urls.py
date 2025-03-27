from rest_framework import routers

from groups.views import GroupViewset, SendGroupInviteViewset

router = routers.DefaultRouter()
router.register(r'invite', SendGroupInviteViewset, basename='group-invite')
router.register(r'', GroupViewset, basename='group')

urlpatterns = router.urls
