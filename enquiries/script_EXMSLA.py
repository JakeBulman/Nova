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
    for task in TaskManager.objects.filter(task_id='RETMIS', task_completion_date__isnull=True):
        extension_total = 0
        exmsla_count = TaskManager.objects.filter(task_id='EXMSLA', ec_sid=task.ec_sid.ec_sid, task_completion_date__isnull=True).count()
        for e in ScriptApportionmentExtension.objects.filter(task_id=TaskManager.objects.get(ec_sid=task.ec_sid,task_id='RETMIS').pk):
            extension_total = int(e.extenstion_days) + extension_total
        slaDate = task.task_creation_date + datetime.timedelta(days=5) + datetime.timedelta(days=extension_total)
        if (slaDate < timezone.now()) and (exmsla_count == 0):
            TaskManager.objects.create(
                enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task.enquiry_id.enquiry_id),
                ec_sid = EnquiryComponents.objects.get(ec_sid=task.ec_sid.ec_sid),
                task_id = 'EXMSLA',
                task_assigned_to = None,
                task_assigned_date = None,
                task_completion_date = None
            )
            TaskManager.objects.filter(pk=task.pk,task_id='RETMIS').update(task_completion_date = timezone.now())  

run_algo()