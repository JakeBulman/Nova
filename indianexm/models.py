from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class IndexmUploads(models.Model):
    document = models.FileField(upload_to='documents/')
    file_name = models.CharField(max_length=50, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
class IndexmUploadData(models.Model):
    file_name = models.CharField(max_length=50, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_downloaded = models.CharField(max_length = 10, null=True) 
    task_assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
class IndexmFileData(models.Model):
    creditor_number = models.CharField(unique=True, max_length = 10, null=True)
    file_key = models.ForeignKey(IndexmUploadData, on_delete=models.SET_NULL, related_name='file_row', null=True)

class IndexmMatches(models.Model):
    creditor_number = models.ForeignKey(IndexmFileData, to_field='creditor_number', on_delete=models.CASCADE, related_name='matched_creditors',null=True)
    is_matched = country_id = models.CharField(max_length = 10, null=True) 
    country_id = models.CharField(max_length = 10, null=True)   

class IndexmSystemData(models.Model):
    creditor_number = models.CharField(max_length = 10, null=True)
    country_id = models.CharField(max_length = 10, null=True)

class IndexmDownloads(models.Model):
    document = models.FileField(upload_to='documents/')
    file_name = models.CharField(max_length=50, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)