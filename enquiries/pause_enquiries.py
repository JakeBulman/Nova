
import sys
import os
import django
from django.utils import timezone
import datetime

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

from enquiries.models import TaskManager, EnquiryComponents, CentreEnquiryRequests, ScriptApportionmentExtension, PausedEnquiry
from django.contrib.auth.models import User

enquiry_list = [
'1323082',
'1323024',
'1323010',
'1322998',
'1322976',
'1322946',
'1322942',
'1322802',
'1322766',
'1322762',
'1322740',
'1322726',
'1322712',
'1322528',
'1322470',
'1322432',
'1322410',
'1322344',
'1322318',
'1322306',
'1322304',
'1322292',
'1322288',
'1322282',
'1322270',
'1322260',
'1322258',
'1322228',
'1322208',
'1322198',
'1322196',
'1322178',
'1322162',
'1322144',
'1322138',
'1322136',
'1322126',
'1322118',
'1322034',
'1322012',
'1321992',
'1321978',
'1321968',
'1321782',
'1321764',
'1321712',
'1321710',
'1321692',
'1321686',
'1321624',
'1321568',
'1321562'
    ]

for enquiry_id in enquiry_list:
    pause_status = 'pause'
    pause_reason = 'Scaling'
    print(enquiry_id)
    if not PausedEnquiry.objects.filter(enquiry_id=enquiry_id):
        PausedEnquiry.objects.create(
            enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
            pause_reason = pause_reason
        )
        TaskManager.objects.filter(enquiry_id=enquiry_id, task_completion_date=None).update(task_assigned_to=User.objects.get(username='PausedEnquiry'),task_completion_date=timezone.now(),task_assigned_date=timezone.now())
