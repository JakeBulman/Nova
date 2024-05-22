from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Datasets(models.Model):
    dataset_name = models.CharField(max_length=30,null=True)
    last_triggered = models.DateTimeField(null=True)
    last_updated = models.DateTimeField(null=True)
    parameter_name = models.CharField(max_length=30,null=True)
    operator = models.CharField(max_length=2,null=True)
    row_count = models.IntegerField(default=0,null=True)
    error_status = models.CharField(max_length=30,null=True)
    sql = models.TextField(null=True)

class ManualTaskQueue(models.Model):
    dataset = models.ForeignKey(Datasets, on_delete=models.CASCADE, related_name='task_queue')
    task_creation_date = models.DateTimeField(auto_now_add=True)
    task_completion_date = models.DateTimeField(null=True)
    task_queued = models.IntegerField(default=1)
    task_running = models.IntegerField(default=0)

class Reports(models.Model):
    report_name = models.CharField(max_length=100,null=True)
    active = models.BooleanField(default=False,null=True)

class Report_Datasets(models.Model):
    report = models.ForeignKey(Reports, on_delete=models.CASCADE, related_name='datasets')
    dataset = models.ForeignKey(Datasets, on_delete=models.CASCADE, related_name='datasets')
    report_parameter = models.CharField(max_length=100,null=True)

class Script_Info(models.Model):
    script = models.CharField(max_length=100,null=True)
    running = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True)