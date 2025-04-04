from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions, status, viewsets
from common.permissions import AdminWriteElseAuthenticated
import restaurants
from .models import Restaurant
from .serializers import RestaurantSerializer
# Create your views here.


class RestaurantView(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [AdminWriteElseAuthenticated]

    