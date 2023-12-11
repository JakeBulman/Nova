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
'1344684',
'1320186',
'1318928',
'1318928',
'1321684',
'1321684',
'1322396',
'1322396',
'1322396',
'1334052',
'1334052',
'1334052',
'1325658',
'1327506',
'1327506',
'1335192',
'1336802',
'1336802',
'1336802',
'1329072',
'1329614',
'1330338',
'1336110',
'1336110',
'1336722',
'1336110',
'1336722',
'1336722',
'1336312',
'1336312',
'1336312',
'1339016',
'1338952',
'1339044',
'1344060',
'1344522',
'1344522',
'1344522',
'1344684',
'1344830',
'1344684',
'1344830',
'1344830',
'1349466',
'1349740',
'1350390',
'1352862',
'1350956',
'1353016',
'1351356',
'1347456',
'1354508',



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