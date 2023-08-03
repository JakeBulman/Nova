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

from enquiries.models import TaskManager, MisReturnData, CentreEnquiryRequests, EnquiryGrades, TaskTypes
from django.contrib.auth.models import User

def run_algo():
    for task in TaskManager.objects.filter(task_id='GRDMAT', task_completion_date__isnull=True):
        enquiry_id = task.enquiry_id.enquiry_id

        #check if grade confirmed, if so skip checks
        script_marks = MisReturnData.objects.filter(ec_sid__erp_sid__cer_sid__enquiry_id=enquiry_id)
        mark_changed_check = 0
        for mark in script_marks:
            if mark.final_mark_status == 'Changed':
                mark_changed_check =+ 1
        print(mark_changed_check)
        if mark_changed_check == 0:
            #mark has not changed, grade has not changed
            TaskManager.objects.create(
                enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
                ec_sid = None,
                task_id = TaskTypes.objects.get(task_id = 'OUTCON'),
                task_assigned_to = None,
                task_assigned_date = None,
                task_completion_date = None
            )
            print('OUTCON')
        else:
            #check if valid grade change value exists, else do nothing
            print("grdcon check 1")
            if EnquiryGrades.objects.filter(enquiry_id=enquiry_id).exists():
                print("grdcon check 2")
                previous_grade = EnquiryGrades.objects.get(enquiry_id=enquiry_id).previous_grade
                new_grade = EnquiryGrades.objects.get(enquiry_id=enquiry_id).new_grade
                if previous_grade == new_grade:
                    #mark has changed, grade has not changed
                    TaskManager.objects.create(
                        enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
                        ec_sid = None,
                        task_id = TaskTypes.objects.get(task_id = 'GRDCON'),
                        task_assigned_to = User.objects.get(username='NovaServer'),
                        task_assigned_date = timezone.now(),
                        task_completion_date = None
                    )
                    print('GRDCON')
                else:
                    #mark has changed, grade has changed
                    TaskManager.objects.create(
                        enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
                        ec_sid = None,
                        task_id = TaskTypes.objects.get(task_id = 'GRDNEG'),
                        task_assigned_to = None,
                        task_assigned_date = None,
                        task_completion_date = None
                    ) 
                    print('GRDNEG')
            else:
                print('no grade avail')
        TaskManager.objects.filter(pk=task.pk,task_id='GRDMAT').update(task_completion_date=timezone.now())   

run_algo()