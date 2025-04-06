from rest_framework import viewsets

from common.permissions import AdminWriteElseAuthenticated
from swipables.models import Swipable

from .models import Restaurant
from .serializers import RestaurantSerializer


class RestaurantView(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [AdminWriteElseAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()
        Swipable.objects.create(restaurant=instance)
