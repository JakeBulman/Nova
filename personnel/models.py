from django.db import models

# Create your models here.
class Personnel(models.Model):
    personnel_name = models.CharField(max_length=100)
    personnel_type = models.CharField(max_length=20)
    employment_start = models.DateField(auto_now=False,auto_now_add=False)
    # employment_end = 