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

from enquiries.models import TaskManager, MisReturnData, CentreEnquiryRequests, EnquiryGrades, TaskTypes, EnquiryRequestParts, EnquiryComponentElements
from django.contrib.auth.models import User

def run_algo():
    for task in TaskManager.objects.filter(task_id='GRDMAT', task_completion_date__isnull=True):
        enquiry_id = task.enquiry_id.enquiry_id

        #check if grade confirmed, if so skip checks
        if MisReturnData.objects.filter(ec_sid__erp_sid__cer_sid__enquiry_id=enquiry_id).exists():
            script_marks = MisReturnData.objects.filter(ec_sid__erp_sid__cer_sid__enquiry_id=enquiry_id)
            mark_changed_check = 0
            for mark in script_marks:
                print(mark.ec_sid.ec_sid)
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
                TaskManager.objects.filter(pk=task.pk,task_id='GRDMAT').update(task_completion_date=timezone.now())
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
                        TaskManager.objects.filter(pk=task.pk,task_id='GRDMAT').update(task_completion_date=timezone.now())
                        print('GRDCON')
                    else:
                        #mark has changed, grade has changed
                        TaskManager.objects.create(
                            enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
                            ec_sid = None,
                            task_id = TaskTypes.objects.get(task_id = 'NEGCON'),
                            task_assigned_to = None,
                            task_assigned_date = None,
                            task_completion_date = None
                        ) 
                        TaskManager.objects.filter(pk=task.pk,task_id='GRDMAT').update(task_completion_date=timezone.now())
                        print('GRDNEG')
                elif EnquiryRequestParts.objects.get(cer_sid=enquiry_id).grade_confirmed_ind == 'Y':
                    #mark has changed, grade has not changed
                    TaskManager.objects.create(
                        enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
                        ec_sid = None,
                        task_id = TaskTypes.objects.get(task_id = 'GRDCON'),
                        task_assigned_to = User.objects.get(username='NovaServer'),
                        task_assigned_date = timezone.now(),
                        task_completion_date = None
                    )
                    TaskManager.objects.filter(pk=task.pk,task_id='GRDMAT').update(task_completion_date=timezone.now())
                    print('GRDCON')
                else:
                    print('no grade avail')
        elif EnquiryRequestParts.objects.get(cer_sid=enquiry_id).service_code in ['1','1S']:
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
                        TaskManager.objects.filter(pk=task.pk,task_id='GRDMAT').update(task_completion_date=timezone.now())
                        print('GRDCON - CLERIC grade present but no change')
                    else:
                        #mark has changed, grade has changed
                        TaskManager.objects.create(
                            enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
                            ec_sid = None,
                            task_id = TaskTypes.objects.get(task_id = 'NEGCON'),
                            task_assigned_to = None,
                            task_assigned_date = None,
                            task_completion_date = None
                        ) 
                        TaskManager.objects.filter(pk=task.pk,task_id='GRDMAT').update(task_completion_date=timezone.now())
                        print('GRDNEG - CLERIC grade present and changed')
                elif EnquiryRequestParts.objects.get(cer_sid=enquiry_id).grade_confirmed_ind == 'Y':
                    #mark has changed, grade has not changed
                    TaskManager.objects.create(
                        enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
                        ec_sid = None,
                        task_id = TaskTypes.objects.get(task_id = 'GRDCON'),
                        task_assigned_to = User.objects.get(username='NovaServer'),
                        task_assigned_date = timezone.now(),
                        task_completion_date = None
                    )
                    TaskManager.objects.filter(pk=task.pk,task_id='GRDMAT').update(task_completion_date=timezone.now())
                    print('GRDCON Grade was confirmed')
                else:
                    if task.task_creation_date + datetime.timedelta(days=7) < timezone.now():
                        clr_needed = []
                        clr_complete = []
                        print('GOT HERE')
                        print(task)
                        for clr in EnquiryComponentElements.objects.filter(ec_sid__erp_sid__cer_sid__enquiry_id=task.enquiry_id.enquiry_id):
                            clr_needed.append(clr.ec_sid.ec_sid)
                        for clr in EnquiryComponentElements.objects.filter(ec_sid__erp_sid__cer_sid__enquiry_id=task.enquiry_id.enquiry_id,clerical_mark_confirmed_ind='Y'):
                            clr_complete.append(clr.ec_sid.ec_sid)     
                        for clr in EnquiryComponentElements.objects.filter(ec_sid__erp_sid__cer_sid__enquiry_id=task.enquiry_id.enquiry_id,omr_mark_confirmed_ind='Y'):
                            clr_complete.append(clr.ec_sid.ec_sid)            
                        for clr in EnquiryComponentElements.objects.filter(ec_sid__erp_sid__cer_sid__enquiry_id=task.enquiry_id.enquiry_id,clerical_mark_changed_ind='Y'):
                            clr_complete.append(clr.ec_sid.ec_sid)  
                        for clr in EnquiryComponentElements.objects.filter(ec_sid__erp_sid__cer_sid__enquiry_id=task.enquiry_id.enquiry_id,omr_mark_changed_ind='Y'):
                            clr_complete.append(clr.ec_sid.ec_sid)  
                        clr_needed.sort()
                        clr_complete.sort()
                        if clr_needed == clr_complete:
                            #mark has changed, grade has not changed and 7 days have passed
                            TaskManager.objects.create(
                                enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
                                ec_sid = None,
                                task_id = TaskTypes.objects.get(task_id = 'GRDCON'),
                                task_assigned_to = User.objects.get(username='NovaServer'),
                                task_assigned_date = timezone.now(),
                                task_completion_date = None
                            )
                            TaskManager.objects.filter(pk=task.pk,task_id='GRDMAT').update(task_completion_date=timezone.now())
                            print('GRDCON - 7 days old')                            
                    else:
                        clr_needed = []
                        clr_complete = []
                        for clr in EnquiryComponentElements.objects.filter(ec_sid__erp_sid__cer_sid__enquiry_id=task.enquiry_id.enquiry_id):
                            clr_needed.append(clr.ec_sid.ec_sid)
                        for clr in EnquiryComponentElements.objects.filter(ec_sid__erp_sid__cer_sid__enquiry_id=task.enquiry_id.enquiry_id,clerical_mark_confirmed_ind='Y'):
                            clr_complete.append(clr.ec_sid.ec_sid)     
                        for clr in EnquiryComponentElements.objects.filter(ec_sid__erp_sid__cer_sid__enquiry_id=task.enquiry_id.enquiry_id,omr_mark_confirmed_ind='Y'):
                            clr_complete.append(clr.ec_sid.ec_sid)             
                        clr_needed.sort()
                        clr_complete.sort()
                        if clr_needed == clr_complete:
                            #mark has not changed, grade has not changed
                            TaskManager.objects.create(
                                enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
                                ec_sid = None,
                                task_id = TaskTypes.objects.get(task_id = 'GRDCON'),
                                task_assigned_to = User.objects.get(username='NovaServer'),
                                task_assigned_date = timezone.now(),
                                task_completion_date = None
                            )
                            TaskManager.objects.filter(pk=task.pk,task_id='GRDMAT').update(task_completion_date=timezone.now())
                            print('GRDCON - all clerics confirmed unchanged')  

        else:
            print('no MIS data')
            #TaskManager.objects.filter(pk=task.pk,task_id='GRDMAT').update(task_completion_date=timezone.now())   

run_algo()