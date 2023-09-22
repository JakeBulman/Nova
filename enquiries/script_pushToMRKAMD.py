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
'1304564',
'1306676',
'1306110',
'1315170',
'1315174',
'1306064',
'1305520',
'1306194',
'1306810',
'1307036',
'1308054',
'1308120',
'1308306',
'1308600',
'1308784',
'1308956',
'1309304',
'1309356',
'1309968',
'1310028',
'1310092',
'1310890',
'1311296',
'1312150',
'1312322',
'1313798',
'1313806',
'1313834',
'1313964',
'1314006',
'1314272',
'1314772',
'1313640',
'1314748',
'1306028',
'1306056',
'1305412',
'1305440',
'1305498',
'1304948',
'1304998',
'1305030',
'1305110',
'1306192',
'1306806',
'1306952',
'1307006',
'1307928',
'1308254',
'1309616',
'1309768',
'1309900',
'1310404',
'1310802',
'1310918',
'1311394',
'1312088',
'1313702',

]

def run_algo():
    for app_task in TaskManager.objects.filter(task_id='GRDREJ', enquiry_id__in = ec_list):
        task_id = app_task.pk
        enquiry_id = TaskManager.objects.get(pk=task_id).enquiry_id.enquiry_id
        if not TaskManager.objects.filter(enquiry_id=enquiry_id, task_id='MRKAMD',task_completion_date = None).exists():
            TaskManager.objects.create(
                enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
                ec_sid = None,
                task_id = TaskTypes.objects.get(task_id = 'MRKAMD'),
                task_assigned_to = None,
                task_assigned_date = None,
                task_completion_date = None
            )

        #complete the task
        TaskManager.objects.filter(pk=task_id,task_id='GRDREJ').update(task_completion_date=timezone.now())    

run_algo()