import sys
import os
import django
from django.utils import timezone
import datetime

if os.getenv('DJANGO_DEVELOPMENT') == 'true':
    path = os.path.join('C:\\Users\\bulmaj\\OneDrive - Cambridge\\Desktop\\Dev\\Nova')
    sys.path.append(path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings_dev'
else:
    sys.path.append('C:/Dev/redepplan')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings'

django.setup()

from enquiries.models import TaskManager, EnquiryComponents, CentreEnquiryRequests, ScriptApportionmentExtension
from django.contrib.auth.models import User

def run_algo():
    for task in TaskManager.objects.filter(task_id='MKWAIT', task_completion_date__isnull=True):

        app_complete_check = None
        #check if completed apportion task is available
        app_complete_check = TaskManager.objects.filter(enquiry_id=task.enquiry_id.enquiry_id,task_id='BOTAPP', task_completion_date__isnull=False)

        if app_complete_check:
            TaskManager.objects.create(
                enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task.enquiry_id.enquiry_id),
                ec_sid = EnquiryComponents.objects.get(ec_sid=task.ec_sid.ec_sid),
                task_id = 'BOTMAR',
                task_assigned_to = User.objects.get(username='RPABOT2'),
                task_assigned_date = timezone.now(),
                task_completion_date = None
            )
                
            TaskManager.objects.filter(pk=task.pk,task_id='MKWAIT').update(task_completion_date=timezone.now())   

run_algo()