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

from enquiries.models import TaskManager, RpaFailureAudit, ScriptApportionment, EnquiryComponentElements, CentreEnquiryRequests, EnquiryComponents, EnquiryComponentsHistory, TaskTypes, ScaledMarks
from django.contrib.auth.models import User

ec_list = ['1961358',
'1961360',
'1958978',
'1960146',
'1961356',
'1957902',
'1957998',
'1958000',
'1958006',
'1958466',
'1958472',
'1958524',
'1958004',
'1958684',
'1958752',
'1958788',
'1958796',
'1958800',
'1958810',
'1959122',
'1958686',
'1961258',
'1961256',
'1958794',
'1958868',
'1958870',
'1958872',
'1958874',
'1957904',
'1958798',
'1963950',
'1963952',
'1958812',
'1958980'
]

def run_algo():
    for app_task in TaskManager.objects.filter(task_id='BOTMAR', ec_sid__in = ec_list):
        enquiry_id = TaskManager.objects.filter(ec_sid=app_task.ec_sid.ec_sid,task_id='BOTMAR').first().enquiry_id.enquiry_id
        #create a new task for the next step (BOTMAF)
        if not TaskManager.objects.filter(enquiry_id=enquiry_id, task_id='BOTMAF',task_completion_date = None).exists():
            this_task = TaskManager.objects.create(
                enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
                ec_sid = EnquiryComponents.objects.get(ec_sid=app_task.ec_sid.ec_sid),
                task_id = TaskTypes.objects.get(task_id = 'BOTMAF'),
                task_assigned_to = User.objects.get(username='LaizPompermaier'),
                task_assigned_date = timezone.now(),
                task_completion_date = None
            )
            this_task.refresh_from_db()
            RpaFailureAudit.objects.create(
                rpa_task_key = TaskManager.objects.get(pk=this_task.pk),
                failure_reason = "Priority Manual Keying"
            )
        #complete the task
        TaskManager.objects.filter(ec_sid=app_task.ec_sid.ec_sid,task_id='BOTMAR').update(task_completion_date=timezone.now())

run_algo()