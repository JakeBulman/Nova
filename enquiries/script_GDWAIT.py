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

from enquiries.models import TaskManager, EnquiryComponents, CentreEnquiryRequests, TaskTypes
from django.contrib.auth.models import User

task_type = ['BOTMAR','BOTMAF','CLERIC','OMRCHE']

def run_algo():
    for task in TaskManager.objects.filter(task_id='GDWAIT', task_completion_date__isnull=True):
        app_complete_check = False
        #check if completed apportion task is available
        enquiry_id = task.enquiry_id.enquiry_id
        comp_list_newmis = []
        for comp in EnquiryComponents.objects.filter(erp_sid__cer_sid=enquiry_id):
            comp_list_newmis.append(comp.ec_sid)
        comp_list_gdwait = []
        for comp in TaskManager.objects.filter(task_id__in=task_type, enquiry_id=enquiry_id, task_completion_date__isnull=False):
            if not TaskManager.objects.filter(task_id__in=task_type, enquiry_id=enquiry_id, task_completion_date__isnull=True).exists():   
                if comp.ec_sid.ec_sid not in comp_list_gdwait:
                    comp_list_gdwait.append(comp.ec_sid.ec_sid)

        comp_list_newmis.sort()
        comp_list_gdwait.sort()

        print(comp_list_newmis,comp_list_gdwait)
        app_complete_check = comp_list_newmis == comp_list_gdwait
        
        if app_complete_check:
            TaskManager.objects.create(
                enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
                ec_sid = None,
                task_id = TaskTypes.objects.get(task_id = 'GRDREL'),
                task_assigned_to = None,
                task_assigned_date = None,
                task_completion_date = None
            )
                
            TaskManager.objects.filter(pk=task.pk,task_id='GDWAIT').update(task_completion_date=timezone.now())   

run_algo()