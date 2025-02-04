from openpyxl import load_workbook
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

from enquiries.models import TaskManager, RpaFailureAudit, ScriptApportionment, EnquiryComponentElements, CentreEnquiryRequests, EnquiryComponents, EnquiryComponentsHistory, TaskTypes, ScaledMarks
from django.contrib.auth.models import User

ec_list = [
'2062128',

]

def run_algo():
    for app_task in TaskManager.objects.filter(task_id='SCRREN', ec_sid__in = ec_list):
        enquiry_id = TaskManager.objects.filter(ec_sid=app_task.ec_sid.ec_sid,task_id='SCRREN').first().enquiry_id.enquiry_id
        script_id = TaskManager.objects.filter(ec_sid=app_task.ec_sid.ec_sid,task_id='SCRREN').first().ec_sid.ec_sid
        print(enquiry_id)
        #create a new task for the next step (BOTMAF)
        if not TaskManager.objects.filter(ec_sid=script_id, task_id='SCRCHE',task_completion_date = None).exists():
            print("Switched")
            this_task = TaskManager.objects.create(
                enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
                ec_sid = EnquiryComponents.objects.get(ec_sid=app_task.ec_sid.ec_sid),
                task_id = TaskTypes.objects.get(task_id = 'SCRCHE'),
                task_assigned_to = None,
                task_assigned_date = None,
                task_completion_date = None
            )
        else:
            print("Not Switched")
        TaskManager.objects.filter(ec_sid=script_id,task_id='SCRREN').update(task_completion_date=timezone.now())

run_algo()