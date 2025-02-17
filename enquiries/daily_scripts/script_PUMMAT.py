import sys
import os
import django
from django.utils import timezone

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

from enquiries.models import TaskManager, CentreEnquiryRequests, TaskTypes
from django.contrib.auth.models import User

def run_algo():
    for task in TaskManager.objects.filter(task_id='PUMMAT', task_completion_date__isnull=True):
        enquiry_id = task.enquiry_id.enquiry_id
        TaskManager.objects.create(
            enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
            ec_sid = None,
            task_id = TaskTypes.objects.get(task_id = 'COMPLT'),
            task_assigned_to = User.objects.get(username='NovaServer'),
            task_assigned_date = timezone.now(),
            task_completion_date = None
        )

        TaskManager.objects.filter(pk=task.pk,task_id='PUMMAT').update(task_completion_date=timezone.now())   

    for task in TaskManager.objects.filter(task_id='LETSCR', task_completion_date__isnull=True):
        enquiry_id = task.enquiry_id.enquiry_id
        TaskManager.objects.filter(enquiry_id=enquiry_id,task_id='LETSCR').update(task_completion_date=timezone.now())   

    for task in TaskManager.objects.filter(task_id='COMPLT', task_completion_date__isnull=True):
        enquiry_id = task.enquiry_id.enquiry_id
        TaskManager.objects.filter(enquiry_id=enquiry_id,task_id='COMPLT').update(task_completion_date=timezone.now())   

run_algo()