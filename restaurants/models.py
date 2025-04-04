from django.db import models
from common.models import TimeStampedModel

# Create your models here.
class Restaurant(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 50)
    category = models.CharField(max_length = 50)
    image = models.ImageField(upload_to='restaurants/', null=True, blank = True)