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
'2062130',
'2062124',
'2064172',
'2063584',
'2063578',
'2063838',
'2063582',
'2063884',
'2064170',
'2064064',
'2064072',
'2064202',
'2064204',
'2064030',
'2064216',
'2064188',
'2064378',
'2064214',
'2064400',
'2064338',
'2064334',
'2064340',
'2064198',
'2064526',
'2064390',
'2064592',
'2064586',
'2064650',
'2064596',
'2064598',
'2064524',
'2064590',
'2064732',
'2064730',
'2064754',
'2064764',
'2064988',
'2064876',
'2064206',
'2062126',
'2064588',
'2064200',
'2063840',
'2064066',
'2064212',
'2066902',
'2066424',
'2064100',
'2063992',
'2064074',
'2064528',
'2064530',
'2064336',
'2064470',
'2064594',
'2066226',
'2066876',
'2066440',
'2066884',
'2064872',
'2066438',
'2067816',
'2067012',
'2067328',
'2066338',
'2067014',
'2066880',
'2066882',
'2064190',
'2066426',
'2063944',
'2066904',
'2064990',
'2066436',
'2066242',
'2067308',
'2066422',
'2063580',
'2064380',
'2064218',
'2064210',
'2064600',
'2067122',
'2066420',
'2066900',
'2066240',
'2067120',
'2070948',
'2066336',
'2072178',
'2066878',
'2064098',
'2071028',
'2070946',
'2070944',
'2072176',
'2064394',
'2064870',
'2067310',
'2071030',
'2071010',
'2072232',
'2064208',
'2070942',
'2072236',
'2073724',
'2074116',
'2074478',
'2075602',
'2073714',
'2070698',
'2073708',
'2074476',
'2074288',
'2073726',
'2066442',
'2067332',
'2073044',
'2074480',
'2073042',
'2074284',
'2073710',
'2073712',
'2074792',
'2073046',
'2074286',
'2067334',
'2067330',
'2076486',
'2076794',
'2064220',
'2076772',
'2076776',
'2073728',
'2073048',
'2064370',
'2076606',
'2076238',
'2076774',
'2074474',
'2076792',
'2064874',
]

def run_algo():
    for app_task in TaskManager.objects.filter(task_id='SCRCHE', ec_sid__in = ec_list):
        enquiry_id = TaskManager.objects.filter(ec_sid=app_task.ec_sid.ec_sid,task_id='SCRCHE').first().enquiry_id.enquiry_id
        script_id = TaskManager.objects.filter(ec_sid=app_task.ec_sid.ec_sid,task_id='SCRCHE').first().ec_sid.ec_sid
        print(enquiry_id)
        #create a new task for the next step (BOTMAF)
        if not TaskManager.objects.filter(enquiry_id=enquiry_id, task_id='SCRAUD',task_completion_date = None).exists():
            print("Switched")
            TaskManager.objects.create(
			enquiry_id = CentreEnquiryRequests.objects.only('enquiry_id').get(enquiry_id=enquiry_id),
			ec_sid = None,
			task_id = TaskTypes.objects.get(task_id = 'SCRAUD'),
			task_assigned_to = None,
			task_assigned_date = None,
			task_completion_date = None
			)
        else:
            print("Not Switched")


run_algo()