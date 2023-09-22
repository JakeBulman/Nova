from openpyxl import load_workbook
import sys
import os
import django
from django.utils import timezone

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
    print('UAT')
    sys.path.append('C:/Dev/redepplan')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings'

django.setup()

from enquiries.models import TaskManager, RpaFailureAudit, ScriptApportionment, EnquiryComponentElements, CentreEnquiryRequests, EnquiryComponents, EnquiryComponentsHistory, TaskTypes, ScaledMarks,GradeFailureAudit
from django.contrib.auth.models import User

ec_list = [
'1958146',
'1955472',
'1955824',
'1957284',
'1958782',
'1958762',
'1959288',
'1944038',
'1941842',
'1941450',
'1954884',
'1957620',
'1955816',
'1959630',
'1958772',
'1959412',
'1957920',
'1960854',
'1960256',
'1951202',

]

def run_algo():
    for app_task in TaskManager.objects.filter(task_id='CLERIC', ec_sid__in = ec_list):
        task_id = app_task.pk
        enquiry_id = TaskManager.objects.get(pk=task_id).enquiry_id.enquiry_id
        if not TaskManager.objects.filter(enquiry_id=enquiry_id, task_id='GDWAIT',task_completion_date = None).exists():
            TaskManager.objects.create(
                enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
                ec_sid = None,
                task_id = TaskTypes.objects.get(task_id = 'GDWAIT'),
                task_assigned_to = None,
                task_assigned_date = None,
                task_completion_date = None
            )

        #complete the task
        TaskManager.objects.filter(pk=task_id,task_id='CLERIC').update(task_completion_date=timezone.now())    

run_algo()