import sys
import os
import django
from django.utils import timezone
import datetime

if os.getenv('DJANGO_DEVELOPMENT') == 'true':
    print('UAT')
    path = os.path.join('C:\\Dev\\Nova')
    sys.path.append(path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings'
elif os.getenv('DJANGO_PRODUCTION') == 'true':
    print('PRD')
    path = os.path.join('C:\\Dev\\Nova')
    sys.path.append(path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings_prod'
else:
    print('DEV')
    path = os.path.join('C:\\Users\\bulmaj\\OneDrive - Cambridge\\Desktop\\Dev\\Nova')
    sys.path.append(path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings_dev'

django.setup()

from enquiries.models import TaskManager, EnquiryComponentElements, CentreEnquiryRequests, TaskTypes
from django.contrib.auth.models import User

def run_algo():
    for task in TaskManager.objects.filter(task_id='CLERIC', task_completion_date__isnull=True):
        enquiry_id = task.enquiry_id.enquiry_id
        for element in EnquiryComponentElements.objects.filter(ec_sid=task.ec_sid.ec_sid):
            if element.clerical_mark_confirmed_ind == 'Y' or element.clerical_mark_changed_ind == 'Y':
                TaskManager.objects.create(
                    enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
                    ec_sid = None,
                    task_id = TaskTypes.objects.get(task_id = 'GDWAIT'),
                    task_assigned_to = None,
                    task_assigned_date = None,
                    task_completion_date = None
                )
                    
                TaskManager.objects.filter(pk=task.pk,task_id='CLERIC').update(task_completion_date=timezone.now(),task_assigned_to=User.objects.get(username='NovaServer'))   

run_algo()