from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = None
    first_name = None
    last_name = None
    username = models.CharField(max_length=50, primary_key=True)
    email = models.EmailField(max_length=50, unique=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
