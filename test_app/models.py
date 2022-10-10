from django.db import models

class Test_employees(models.Model):
    employee_name = models.CharField(max_length=100, blank=True)
    employee_ID = models.CharField(max_length=20)
    employee_location = models.CharField(max_length=200)
