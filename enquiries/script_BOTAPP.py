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
    print('UAT - Check')
    path = os.path.join('C:\\Dev\\nova')
    sys.path.append(path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings'

django.setup()

from enquiries.models import TaskManager, EnquiryComponents, CentreEnquiryRequests, TaskTypes, ScriptApportionment
from django.contrib.auth.models import User

task_type = ['BOTMAR','BOTMAF','CLERIC','OMRCHE']

def run_algo():
    for task in TaskManager.objects.filter(task_id='BOTAPP', task_completion_date__isnull=True):

        script_apportion_details = ScriptApportionment.objects.get(ec_sid=task.ec_sid.ec_sid,apportionment_invalidated=0)
        
                
        TaskManager.objects.filter(pk=task.pk,task_id='BOTAPP').update(task_completion_date=timezone.now())   

run_algo()