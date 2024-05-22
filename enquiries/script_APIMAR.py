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

from enquiries.models import TaskManager, ScriptApportionment,EnquiryComponentElements, DjangoStagingTable
from django.contrib.auth.models import User

def run_algo():
    for task in TaskManager.objects.filter(task_id='APIMAR', task_completion_date__isnull=True):

        script_apportion_details = ScriptApportionment.objects.get(ec_sid=task.ec_sid.ec_sid,apportionment_invalidated=0)

        enpe_sid = script_apportion_details.enpe_sid
        ec_sid = script_apportion_details.ec_sid
        eb_sid = EnquiryComponentElements.objects.filter(ec_sid=ec_sid).first().eb_sid
        per_sid = script_apportion_details.enpe_sid.per_sid.per_sid
        pan_sid = script_apportion_details.enpe_sid.sp_sid

        print("Start")
        print(enpe_sid)
        print(ec_sid)
        print(eb_sid)
        print(per_sid)
        print(pan_sid)

        if DjangoStagingTable.objects.filter(ec_sid=ec_sid,copied_to_est=0).exists():
            DjangoStagingTable.objects.filter(ec_sid=ec_sid,copied_to_est=0).update(
                enpe_sid = enpe_sid,
                ec_sid = ec_sid,
                eb_sid = eb_sid,
                per_sid = per_sid,
                pan_sid = pan_sid
            )
        else:
            DjangoStagingTable.objects.create(
                enpe_sid = enpe_sid,
                ec_sid = ec_sid,
                eb_sid = eb_sid,
                per_sid = per_sid,
                pan_sid = pan_sid
            )


        #TaskManager.objects.filter(pk=task.pk,task_id='APIAPP').update(task_completion_date=timezone.now())   

run_algo()