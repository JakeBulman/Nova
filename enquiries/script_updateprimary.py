from openpyxl import load_workbook
import sys
import os
import django
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

from enquiries.models import TaskTeams, TaskTypes, TaskUserPrimary, TaskUserSecondary
from django.contrib.auth.models import User



def load_core_tables():

    start_time = datetime.datetime.now()
    print("Start Time:" + str(datetime.datetime.now()))

    username = 'admin'
    teamname = 'Server'
    status = 'TL'
    TaskUserPrimary.objects.create(
        task_user = User.objects.get(username=username),
        primary_team = TaskTeams.objects.get(team_name=teamname),
        primary_status = status
    )

    end_time = datetime.datetime.now()
    print(end_time - start_time)

load_core_tables()