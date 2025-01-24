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
'2088494',
'2087640',
'2086014',
'2082116',
'2082102',
'2082112',
'2082108',
'2082104',
'2082114',
'2082088',
'2082070',
'2082072',
'2082046',
'2082036',
'2081970',
'2081918',
'2081912',
'2081910',
'2081888',
'2081890',
'2081868',
'2081858',
'2081862',
'2081850',
'2081840',
'2081830',
'2081790',
'2081770',
'2081746',
'2081734',
'2081732',
'2081740',
'2081736',
'2081726',
'2081674',
'2081662',
'2081666',
'2081658',
'2081648',
'2081646',
'2081640',
'2081636',
'2081638',
'2081620',
'2081486',
'2081454',
'2077626',
'2073556',
'2072320',
'2069508',
'2067722',
'2067424',
'2066580',
'2079780',
'2079792',
'2079762',
'2079680',
'2074548',
'2079420',
'2093336',
'2076450',
'2076402',
'2076390',
'2076392',
'2076386',
'2076378',
'2076370',
'2076358',
'2076360',
'2076342',
'2076344',
'2076338',
'2076348',
'2076346',
'2076340',
'2076332',
'2076334',
'2076326',
'2076316',
'2076318',
'2076314',
'2076298',
'2076296',
'2076312',
'2076306',
'2076302',
'2076308',
'2076294',
'2076310',
'2076272',
'2076276',
'2076274',
'2076270',
'2076266',
'2076264',
'2076246',
'2076250',
'2076248',
'2076234',
'2076242',
'2076232',
'2076240',
'2076236',
'2076228',
'2076244',
'2076218',
'2076200',
'2076226',
'2076224',
'2076212',
'2066906',
'2076776',
'2073708',
'2067328',
'2066882',
'2066880',
'2066438',
'2064214',
'2064206',
'2063582',
'2072166',
'2072164',
'2072128',
'2072126',
'2072124',
'2072120',
'2072132',
'2072122',
'2072108',
'2072106',
'2072096',
'2072094',
'2072082',
'2072084',
'2072070',
'2072034',
'2072024',
'2072026',
'2072022',
'2071998',
'2071994',
'2071992',
'2071982',
'2071976',
'2071984',
'2071986',
'2071988',
'2071996',
'2071990',
'2072002',
'2071962',
'2071958',
'2071966',
'2071956',
'2071960',
'2071938',
'2071936',
'2071932',
'2071934',
'2071924',
'2071906',
'2071900',
'2071904',
'2071898',
'2071902',
'2071882',
'2071884',
'2067010',
'2066520',
'2062678'
]

def run_algo():
    for script in ec_list:
        print(script)
        enquiry_id = TaskManager.objects.filter(ec_sid=script,task_id='SCRREN').first().enquiry_id.enquiry_id
        if not TaskManager.objects.filter(enquiry_id=enquiry_id, task_id='ESMSC2',task_completion_date = None).exists():
            TaskManager.objects.create(
			enquiry_id = CentreEnquiryRequests.objects.only('enquiry_id').get(enquiry_id=enquiry_id),
			ec_sid = EnquiryComponents.objects.get(ec_sid=script),
			task_id = TaskTypes.objects.get(task_id = 'ESMSC2'),
			task_assigned_to = None,
			task_assigned_date = None,
			task_completion_date = None
			)




run_algo()