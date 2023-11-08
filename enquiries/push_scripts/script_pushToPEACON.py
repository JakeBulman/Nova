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

ec_list = ['1302628',
'1304948',
'1305030',
'1303670',
'1306028',
'1305440',
'1305498',
'1306952',
'1305412',
'1303494',
'1303918',
'1304138',
'1306192',
'1307928',
'1302972',
'1306056',
'1305110',
'1306806',
'1307006',
'1304980',
'1308254',
'1304998',
'1306262',
'1309616',
'1309900',
'1309768',
'1310918',
'1310802',
'1310404',
'1311394',
'1312088',
'1313640',
'1314748',

]

def run_algo():
    for app_task in TaskManager.objects.filter(task_id='NEGCON', enquiry_id__in = ec_list):
        task_id = app_task.pk
        enquiry_id = TaskManager.objects.get(pk=task_id).enquiry_id.enquiry_id
        # if not TaskManager.objects.filter(enquiry_id=enquiry_id, task_id='PEACON',task_completion_date = None).exists():
        #     TaskManager.objects.create(
        #         enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
        #         ec_sid = None,
        #         task_id = TaskTypes.objects.get(task_id = 'PEACON'),
        #         task_assigned_to = None,
        #         task_assigned_date = None,
        #         task_completion_date = None
        #     )

        if not TaskManager.objects.filter(enquiry_id=enquiry_id, task_id='GRDREJ',task_completion_date = None).exists():
            new_task = TaskManager.objects.create(
                enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
                ec_sid = None,
                task_id = TaskTypes.objects.get(task_id = 'GRDREJ'),
                task_assigned_to = None,
                task_assigned_date = None,
                task_completion_date = None
            )
            GradeFailureAudit.objects.create(
				task_key = TaskManager.objects.get(pk=new_task.pk),
				failure_stage = TaskTypes.objects.get(task_id='NEGCON'),
				failure_reason = 'Numeric Grade Change' 
            )		

        #complete the task
        TaskManager.objects.filter(pk=task_id,task_id='NEGCON').update(task_completion_date=timezone.now())    

run_algo()