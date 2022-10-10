from django.db import models

# Create your models here.
class Centres(models.Model):
    Centre_name = models.CharField(max_length=100, blank=True)
    Centre_ID = models.CharField(max_length=20)
    Centre_location = models.CharField(max_length=200)
    is_open = models.BooleanField()

