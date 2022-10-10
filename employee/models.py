from django.db import models

class Employee(models.Model):
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    full_years_of_service = models.IntegerField()
    height_meters = models.DecimalField(max_digits=3, decimal_places=2)
    on_probation = models.BooleanField()

