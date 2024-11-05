import sys
import os
import django

 

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
    #sys.path.append('C:/Dev/redepplan') -- Jake Local
    sys.path.append('C:/Users/rfrancisco/Desktop/Dev Folder/EAR/Nova/')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings'
    #os.environ.setdefault('DJANGO_SETTINGS_MODULE','redepplan.settings')
    
django.setup()

from django.contrib.auth.models import User
from enquiries.models import EarServerSettings, TaskUserPrimary, TaskTeams

if EarServerSettings.objects.all().count() == 0:
    EarServerSettings.objects.create(
            session_id_list = "19848",
            enquiry_id_list = "",
        )
if TaskTeams.objects.all().count() == 0:
    TaskTeams.objects.create(
        team_name='Server',
    )

if TaskUserPrimary.objects.filter(task_user=1).exists():
    pass
else:
    TaskUserPrimary.objects.create(
        primary_status = "CO",
        primary_team_id = TaskTeams.objects.get(team_name='Server').pk,
        task_user_id = 1
    )

