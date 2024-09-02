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

def run_algo():
    for task in TaskManager.objects.filter(task_id='MKWAIT', task_completion_date__isnull=True):

        app_complete_check = None
        #check if completed apportion task is available
        #TODO: check if on an error path such as being reapped or bot failed
        task_list = ['BOTAPP','NRMACC','REMAPF','BOTAPF','S3CONF']
        script_id = task.ec_sid.ec_sid
        app_complete_check = TaskManager.objects.filter(enquiry_id=task.enquiry_id.enquiry_id,task_id__in=task_list, task_completion_date__isnull=False)
        #app_complete_check2 = TaskManager.objects.filter(enquiry_id=task.enquiry_id.enquiry_id,task_id = 'BOTAPP', task_completion_date__isnull=False) and TaskManager.objects.filter(enquiry_id=task.enquiry_id.enquiry_id,task_id = 'BOTAPF', task_completion_date__isnull=True)
        if app_complete_check:
            if not TaskManager.objects.filter(ec_sid=script_id, task_id='BOTMAR',task_completion_date = None).exists():
                TaskManager.objects.create(
                    enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task.enquiry_id.enquiry_id),
                    ec_sid = EnquiryComponents.objects.get(ec_sid=task.ec_sid.ec_sid),
                    task_id = TaskTypes.objects.get(task_id = 'BOTMAR'),
                    task_assigned_to = User.objects.get(username='RPABOT2'),
                    task_assigned_date = timezone.now(),
                    task_completion_date = None
                )
            if EnquiryComponents.objects.only('ec_sid').get(ec_sid=script_id).erp_sid.service_code == '2S' or EnquiryComponents.objects.only('ec_sid').get(ec_sid=script_id).erp_sid.service_code == '2PS':
                if EnquiryComponents.objects.only('ec_sid').get(ec_sid=script_id).script_type == 'RM Assessor':
                    if not TaskManager.objects.filter(ec_sid=script_id, task_id='ESMSC2',task_completion_date = None).exists():
                        TaskManager.objects.create(
                            enquiry_id = CentreEnquiryRequests.objects.only('enquiry_id').get(enquiry_id=task.enquiry_id.enquiry_id),
                            ec_sid = EnquiryComponents.objects.only('ec_sid').get(ec_sid=script_id),
                            task_id = TaskTypes.objects.get(task_id = 'ESMSC2'),
                            task_assigned_to = None,
                            task_assigned_date = None,
                            task_completion_date = None
                        )
                else:
                    if not TaskManager.objects.filter(ec_sid=script_id, task_id='SCRCHE').exists():
                        TaskManager.objects.create(
                            enquiry_id = CentreEnquiryRequests.objects.only('enquiry_id').get(enquiry_id=task.enquiry_id.enquiry_id),
                            ec_sid = EnquiryComponents.objects.only('ec_sid').get(ec_sid=script_id),
                            task_id = TaskTypes.objects.get(task_id = 'SCRCHE'),
                            task_assigned_to = None,
                            task_assigned_date = None,
                            task_completion_date = None
                        )
                    
            TaskManager.objects.filter(pk=task.pk,task_id='MKWAIT').update(task_completion_date=timezone.now()) 

run_algo()