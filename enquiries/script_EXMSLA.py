import sys
import os
import django
from django.utils import timezone
import datetime

if os.getenv('DJANGO_DEVELOPMENT') == 'true':
    print('DEV')
    path = os.path.join('C:\\Users\\bulmaj\\OneDrive - Cambridge\\Desktop\\Dev\\Nova')
    sys.path.append(path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings_dev'
elif os.getenv('DJANGO_PRODUCTION') == 'true':
    print('PROD')
    path = os.path.join('C:\\Dev\\Nova')
    sys.path.append(path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings_prod'
else:
    print('UAT - Check')
    path = os.path.join('C:\\Dev\\nova')
    sys.path.append(path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings'

django.setup()

from enquiries.models import TaskManager, EnquiryComponents, CentreEnquiryRequests, ScriptApportionmentExtension, TaskTypes
from django.contrib.auth.models import User

def run_algo():
    for task in TaskManager.objects.filter(task_id='RETMIS', task_completion_date__isnull=True):
        extension_total = 0
        exmsla_count = TaskManager.objects.filter(task_id='EXMSLA', ec_sid=task.ec_sid.ec_sid, task_completion_date__isnull=True).count()
        for e in ScriptApportionmentExtension.objects.filter(ec_sid=task.ec_sid.ec_sid):
            extension_total = int(e.extension_days) + extension_total
        slaDate = task.task_creation_date + datetime.timedelta(days=5) + datetime.timedelta(days=extension_total)
        if (slaDate < timezone.now()) and (exmsla_count == 0):
            TaskManager.objects.create(
                enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task.enquiry_id.enquiry_id),
                ec_sid = EnquiryComponents.objects.get(ec_sid=task.ec_sid.ec_sid),
                task_id = TaskTypes.objects.get(task_id = 'EXMSLA'),
                task_assigned_to = None,
                task_assigned_date = None,
                task_completion_date = None
            )
    #Remove EXMSLA where no RETMIS are left open.
    for task in TaskManager.objects.filter(task_id='EXMSLA', task_completion_date__isnull=True):
        retmis_closed_check = TaskManager.objects.filter(task_id='RETMIS', ec_sid=task.ec_sid.ec_sid, task_completion_date__isnull=True).count()
        retmis_open_check = TaskManager.objects.filter(task_id='RETMIS', ec_sid=task.ec_sid.ec_sid, task_completion_date__isnull=False).count()
        if retmis_closed_check > 0 and retmis_open_check == 0:
            TaskManager.objects.filter(pk=task.pk,task_id='EXMSLA').update(task_completion_date=timezone.now())   
run_algo()