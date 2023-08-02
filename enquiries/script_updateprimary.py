from openpyxl import load_workbook
import sys
import os
import django
import datetime

if os.getenv('DJANGO_DEVELOPMENT') == 'true':
    path = os.path.join('C:\\Users\\bulmaj\\OneDrive - Cambridge\\Desktop\\Dev\\Nova')
    sys.path.append(path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings_dev'
else:
    sys.path.append('C:/Dev/redepplan')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings'

django.setup()

from enquiries.models import TaskTeams, TaskTypes, TaskUserPrimary, TaskUserSecondary
from django.contrib.auth.models import User



def load_core_tables():

    start_time = datetime.datetime.now()
    print("Start Time:" + str(datetime.datetime.now()))
    username = 'JakeBulman'
    teamname = 'Server'
    status = 'TL'
    print(str(TaskUserPrimary.objects.filter(task_user_id=User.objects.get(username=username).pk).exists()))
    if TaskUserPrimary.objects.filter(task_user_id=User.objects.get(username=username).pk).exists():
        TaskUserPrimary.objects.filter(task_user_id=User.objects.get(username=username).pk).update(            
            primary_team = TaskTeams.objects.get(team_name=teamname),
            primary_status = status)
    else:
        TaskUserPrimary.objects.create(
            task_user = User.objects.get(username=username),
            primary_team = TaskTeams.objects.get(team_name=teamname),
            primary_status = status
        )

    end_time = datetime.datetime.now()
    print(end_time - start_time)

load_core_tables()