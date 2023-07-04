import sys
import os
import django
from django.utils import timezone
import datetime


sys.path.append('C:/Dev/redepplan')
os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings'
django.setup()
from enquiries.models import TaskManager, EnquiryComponents, CentreEnquiryRequests, ScriptApportionmentExtension
from django.contrib.auth.models import User

def run_algo():
    for task in TaskManager.objects.filter(task_id='GRDNEG', task_completion_date__isnull=False):
        # TODO: actually check if grade is negative...
        enquiry_id = task.enquiry_id.enquiry_id


        TaskManager.objects.create(
            enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
            ec_sid = None,
            task_id = 'NEGCON',
            task_assigned_to = None,
            task_assigned_date = None,
            task_completion_date = None
        ) 

        TaskManager.objects.filter(pk=task.pk,task_id='GRDNEG').update(task_completion_date=timezone.now())   

run_algo()