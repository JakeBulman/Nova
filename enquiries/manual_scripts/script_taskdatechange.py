from openpyxl import load_workbook
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

from enquiries.models import TaskManager, RpaFailureAudit, ScriptApportionment, EnquiryComponentElements, CentreEnquiryRequests, EnquiryComponents, EnquiryComponentsHistory, TaskTypes, ScaledMarks,GradeFailureAudit
from django.contrib.auth.models import User

ec_list = [
'2035580',
'2035662',


]

def run_algo():
    for app_task in TaskManager.objects.filter(task_id='RETMIS', ec_sid__in = ec_list, task_completion_date__isnull=True):

        new_creation_date = app_task.task_creation_date + datetime.timedelta(1)
        new_assigned_date = app_task.task_assigned_date + datetime.timedelta(1)

        app_task.task_creation_date = new_creation_date
        app_task.task_assigned_date = new_assigned_date

        app_task.save()


run_algo()