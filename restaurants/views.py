from rest_framework import viewsets
from rest_framework import viewsets
from common.permissions import AdminWriteElseAuthenticated
from .models import Restaurant
from .serializers import RestaurantSerializer
# Create your views here.


class RestaurantView(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [AdminWriteElseAuthenticated]

    