from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import SwipableListView, SwipeViewset

router = DefaultRouter()
router.register(r'swipes', SwipeViewset, basename='swipe')

urlpatterns = [
    path('', SwipableListView.as_view(), name='swipables'),
    *router.urls,
]
