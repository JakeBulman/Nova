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

ec_list = [
]

def run_algo():
    for app_task in TaskManager.objects.filter(task_id='SCRREN'):
        task_id = app_task.pk
        enquiry_id = TaskManager.objects.get(pk=task_id).enquiry_id.enquiry_id
        script_id = TaskManager.objects.get(pk=task_id).ec_sid.ec_sid
        service_code = EnquiryComponents.objects.only('ec_sid').get(ec_sid=script_id).erp_sid.service_code
        if service_code == 'ASC' or service_code == 'ASR' or '1' in service_code:
            if not TaskManager.objects.filter(ec_sid=script_id, task_id='ESMSCR',task_completion_date = None).exists():
                TaskManager.objects.create(
                    enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
                    ec_sid = EnquiryComponents.objects.get(ec_sid=script_id),
                    task_id = TaskTypes.objects.get(task_id = 'ESMSCR'),
                    task_assigned_to = None,
                    task_assigned_date = None,
                    task_completion_date = None
                )  
        else:
            if not TaskManager.objects.filter(ec_sid=script_id, task_id='ESMSC2',task_completion_date = None).exists():
                TaskManager.objects.create(
                    enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
                    ec_sid = EnquiryComponents.objects.get(ec_sid=script_id),
                    task_id = TaskTypes.objects.get(task_id = 'ESMSC2'),
                    task_assigned_to = None,
                    task_assigned_date = None,
                    task_completion_date = None
                )
        #complete the task
        TaskManager.objects.filter(pk=task_id,task_id='SCRREN').update(task_completion_date=timezone.now())    

run_algo()