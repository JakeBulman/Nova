import sys
import os
import django
from django.utils import timezone
import datetime

if os.getenv('DJANGO_DEVELOPMENT') == 'true':
    path = os.path.join('C:\\Users\\bulmaj\\OneDrive - Cambridge\\Desktop\\Dev\\Nova')
    sys.path.append(path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings_dev'
else:
    sys.path.append('C:/Dev/redepplan')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings'

django.setup()

from enquiries.models import TaskManager, EnquiryComponents, CentreEnquiryRequests, ScriptApportionmentExtension
from django.contrib.auth.models import User

def run_algo():
    for task in TaskManager.objects.filter(task_id='GRDMAT', task_completion_date__isnull=True):
        # TODO: actually check if grades exist...
        enquiry_id = task.enquiry_id.enquiry_id
        grade_exists = True

        





        if grade_exists:
            grade_change_check = True
            if grade_change_check:
                TaskManager.objects.create(
                    enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
                    ec_sid = None,
                    task_id = 'GRDNEG',
                    task_assigned_to = User.objects.get(id=33),
                    task_assigned_date = timezone.now(),
                    task_completion_date = None
                )
            else:
                TaskManager.objects.create(
                    enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
                    ec_sid = None,
                    task_id = 'GRDCON',
                    task_assigned_to = None,
                    task_assigned_date = None,
                    task_completion_date = None
                ) 

        TaskManager.objects.filter(pk=task.pk,task_id='GRDMAT').update(task_completion_date=timezone.now())   

run_algo()