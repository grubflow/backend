from uuid import uuid4

from django.utils import timezone
from PIL import Image
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        exclude = ['groups', 'user_permissions']

    def validate_image(self, value):
        if not value:
            return value

        if not hasattr(value, 'name'):
            raise ValidationError("Invalid file type. Please upload an image.")

        image = Image.open(value)
        if image.width != 400 or image.height != 400:
            raise ValidationError("Image must be exactly 400x400 pixels.")

        extension = value.name.split('.')[-1].lower()
        new_name = f"{uuid4().hex}.{extension}"
        value.name = new_name

        return value

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
            instance.save()

        return super().update(instance, validated_data)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.last_login = timezone.now()
        user.save()

        return user
