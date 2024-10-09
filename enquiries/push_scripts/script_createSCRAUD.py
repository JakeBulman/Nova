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
'1386964',
'1385958',
'1383712',
'1383702',
'1383710',
'1383706',
'1383694',
'1383680',
'1383658',
'1383600',
'1383556',
'1383540',
'1383542',
'1383528',
'1383520',
'1383524',
'1383474',
'1383436',
'1383438',
'1383396',
'1383390',
'1383388',
'1383382',
'1383378',
'1383380',
'1382396',
'1379318',
'1380432',
'1380408',
'1380400',
'1380392',
'1380384',
'1380378',
'1380370',
'1380372',
'1380368',
'1380362',
'1380364',
'1380356',
'1380350',
'1380348',
'1380334',
'1380346',
'1380342',
'1380338',
'1380344',
'1380332',
'1380320',
'1380322',
'1380318',
'1380314',
'1380304',
'1380306',
'1380294',
'1380300',
'1380292',
'1380298',
'1380288',
'1380302',
'1380268',
'1380286',
'1380284',
'1380274',
'1377990',
'1377972',
'1377970',
'1377968',
'1377962',
'1377960',
'1377956',
'1377954',
'1377948',
'1377940',
'1377922',
'1377918',
'1377904',
'1377902',
'1377898',
'1377894',
'1377900',
'1377886',
'1377884',
'1377876',
'1377874',
'1377868',
'1377856',
'1377852',
'1377854',
'1377844',
'1375104',
'1372634',
]

def run_algo():
    for enquiry_id in ec_list:
        if not TaskManager.objects.filter(enquiry_id=enquiry_id, task_id='SCRAUD',task_completion_date = None).exists():
            TaskManager.objects.create(
			enquiry_id = CentreEnquiryRequests.objects.only('enquiry_id').get(enquiry_id=enquiry_id),
			ec_sid = None,
			task_id = TaskTypes.objects.get(task_id = 'SCRAUD'),
			task_assigned_to = None,
			task_assigned_date = None,
			task_completion_date = None
			)




run_algo()