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


]

def run_algo():
    for app_task in TaskManager.objects.filter(task_id='BOTAPP', ec_sid__in = ec_list,task_completion_date = None):
        enquiry_id = TaskManager.objects.filter(ec_sid=app_task.ec_sid.ec_sid,task_id='BOTAPP').first().enquiry_id.enquiry_id
        script_id = TaskManager.objects.filter(ec_sid=app_task.ec_sid.ec_sid,task_id='BOTAPP').first().ec_sid.ec_sid
        print(enquiry_id)
        #create a new task for the next step (BOTMAF)
        if not TaskManager.objects.filter(ec_sid=script_id, task_id='BOTAPF',task_completion_date = None).exists():
            print("Switched")
            this_task = TaskManager.objects.create(
                enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
                ec_sid = EnquiryComponents.objects.get(ec_sid=app_task.ec_sid.ec_sid),
                task_id = TaskTypes.objects.get(task_id = 'BOTAPF'),
                task_assigned_to = None,
                task_assigned_date = None,
                task_completion_date = None
            )
            this_task.refresh_from_db()
            RpaFailureAudit.objects.create(
                rpa_task_key = TaskManager.objects.get(pk=this_task.pk),
                failure_reason = "Priority Manual Keying"
            )
            #complete the task
            TaskManager.objects.filter(ec_sid=app_task.ec_sid.ec_sid,task_id='BOTAPP').update(task_completion_date=timezone.now())
        else:
            print("Not Switched")


run_algo()