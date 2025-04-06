from uuid import uuid4

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

    def validate_image(self, value):
        if not value:
            return value

        if not hasattr(value, 'name'):
            raise ValidationError("Invalid file type. Please upload an image.")

        extension = value.name.split('.')[-1].lower()
        new_name = f"{uuid4().hex}.{extension}"
        value.name = new_name

        return value
