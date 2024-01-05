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
    print('UAT - Check')
    path = os.path.join('C:\\Dev\\nova')
    sys.path.append(path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings'

django.setup()

from enquiries.models import TaskManager, RpaFailureAudit, ScriptApportionment, EnquiryComponentElements, CentreEnquiryRequests, EnquiryComponents, EnquiryComponentsHistory, TaskTypes, ScaledMarks,GradeFailureAudit
from django.contrib.auth.models import User

ec_list = [
'1318140',
'1318348',
'1318350',
'1321362',
'1318352',
'1324734',
'1324332',
'1321772',
'1319794',
'1323086',
'1333366',
'1325514',
'1326226',
'1324014',
'1326824',
'1322848',
'1325088',
'1335790',
'1337498',
'1328344',
'1328728',
'1329086',
'1330130',
'1330376',
'1330758',
'1331124',
'1331364',
'1336552',
'1340374',
'1341436',
'1342026',
'1343828',
'1345512',
'1345592',
'1349086',
'1352552',
'1347068',
'1351334',
'1351394',
'1351558',
'1349408',

]

def run_algo():
    for app_task in TaskManager.objects.filter(task_id='PDACON', enquiry_id__in = ec_list):
        task_id = app_task.pk
        enquiry_id = TaskManager.objects.get(pk=task_id).enquiry_id.enquiry_id
        # if not TaskManager.objects.filter(enquiry_id=enquiry_id, task_id='GRDCHG',task_completion_date = None).exists():
        #     TaskManager.objects.create(
        #         enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
        #         ec_sid = None,
        #         task_id = TaskTypes.objects.get(task_id = 'GRDCHG'),
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
				failure_stage = TaskTypes.objects.get(task_id='PDACON'),
				failure_reason = 'Rejected by PM' 
            )		

        #complete the task
        TaskManager.objects.filter(pk=task_id,task_id='PDACON').update(task_completion_date=timezone.now())    

run_algo()