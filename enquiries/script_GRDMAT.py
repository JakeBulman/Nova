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

from enquiries.models import TaskManager, MisReturnData, CentreEnquiryRequests, EnquiryGrades, TaskTypes, EnquiryRequestParts, EnquiryComponentElements, EnquiryComponentsPreviousExaminers
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
                    enquiry_id_id = enquiry_id,
                    ec_sid = None,
                    task_id_id = 'COMPLT',
                    task_assigned_to = User.objects.get(username='NovaServer'),
                    task_assigned_date = timezone.now(),
                    task_completion_date = timezone.now()
                )
                TaskManager.objects.filter(pk=task.pk,task_id='GRDMAT').update(task_completion_date=timezone.now())
            else:
                #check if valid grade change value exists, else do nothing
                if EnquiryGrades.objects.filter(enquiry_id=enquiry_id).exists():
                    previous_grade = EnquiryGrades.objects.get(enquiry_id=enquiry_id).previous_grade
                    new_grade = EnquiryGrades.objects.get(enquiry_id=enquiry_id).new_grade
                    if previous_grade == new_grade:
                        #mark has changed, grade has not changed
                        TaskManager.objects.create(
                            enquiry_id_id = enquiry_id,
                            ec_sid = None,
                            task_id_id = 'COMPLT',
                            task_assigned_to = User.objects.get(username='NovaServer'),
                            task_assigned_date = timezone.now(),
                            task_completion_date = timezone.now()
                        )
                        TaskManager.objects.filter(pk=task.pk,task_id='GRDMAT').update(task_completion_date=timezone.now())
                    else:
                        previous_seq = EnquiryGrades.objects.get(enquiry_id=enquiry_id).previous_seq
                        if previous_seq is None:
                            previous_seq = ''
                        new_seq = EnquiryGrades.objects.get(enquiry_id=enquiry_id).new_seq
                        if new_seq is None:
                            new_seq = ''
                        if previous_seq < new_seq:
                            #mark has changed, grade has changed, grade is negative
                            TaskManager.objects.create(
                                enquiry_id_id = CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
                                ec_sid = None,
                                task_id_id = TaskTypes.objects.get(task_id = 'GRDREJ'),
                                task_assigned_to = None,
                                task_assigned_date = None,
                                task_completion_date = None
                            ) 
                        else:
                            #mark has changed, grade has changed, grade is positive
                            #check if any script was marked by PE
                            if EnquiryComponentsPreviousExaminers.objects.filter(cer_sid=enquiry_id,exm_position='01.01').exists():
                                TaskManager.objects.create(
                                enquiry_id_id = enquiry_id,
                                ec_sid = None,
                                task_id_id = 'PEACON',
                                task_assigned_to = None,
                                task_assigned_date = None,
                                task_completion_date = None
                                )  
                            else:
                                TaskManager.objects.create(
                                enquiry_id_id = enquiry_id,
                                ec_sid = None,
                                task_id_id = 'PDACON',
                                task_assigned_to = None,
                                task_assigned_date = None,
                                task_completion_date = None
                                )

                elif EnquiryRequestParts.objects.get(cer_sid=enquiry_id).grade_confirmed_ind == 'Y':
                    #mark has changed, grade has not changed
                    TaskManager.objects.create(
                        enquiry_id_id = enquiry_id,
                        ec_sid = None,
                        task_id_id = 'COMPLT',
                        task_assigned_to = User.objects.get(username='NovaServer'),
                        task_assigned_date = timezone.now(),
                        task_completion_date = timezone.now()
                    )
                    TaskManager.objects.filter(pk=task.pk,task_id='GRDMAT').update(task_completion_date=timezone.now())
                else:
                    print('no grade avail')
        elif EnquiryRequestParts.objects.get(cer_sid=enquiry_id).service_code in ['1','1S']:
                #check if valid grade change value exists, else do nothing
                if EnquiryGrades.objects.filter(enquiry_id=enquiry_id).exists():
                    previous_grade = EnquiryGrades.objects.get(enquiry_id=enquiry_id).previous_grade
                    new_grade = EnquiryGrades.objects.get(enquiry_id=enquiry_id).new_grade
                    if previous_grade == new_grade:
                        #mark has changed, grade has not changed
                        TaskManager.objects.create(
                            enquiry_id_id = enquiry_id,
                            ec_sid = None,
                            task_id_id = 'COMPLT',
                            task_assigned_to = User.objects.get(username='NovaServer'),
                            task_assigned_date = timezone.now(),
                            task_completion_date = timezone.now()
                        )
                        TaskManager.objects.filter(pk=task.pk,task_id='GRDMAT').update(task_completion_date=timezone.now())
                    else:
                        previous_seq = EnquiryGrades.objects.get(enquiry_id=enquiry_id).previous_seq
                        new_seq = EnquiryGrades.objects.get(enquiry_id=enquiry_id).new_seq
                        if previous_seq < new_seq:
                            #mark has changed, grade has changed, grade is negative
                            TaskManager.objects.create(
                                enquiry_id_id = enquiry_id,
                                ec_sid = None,
                                task_id_id = 'GRDREJ',
                                task_assigned_to = None,
                                task_assigned_date = None,
                                task_completion_date = None
                            ) 
                        else:
                            #mark has changed, grade has changed, grade is positive
                            #check if any script was marked by PE
                            if EnquiryComponentsPreviousExaminers.objects.filter(enquiry_id=enquiry_id,exm_position='01.01').exists():
                                TaskManager.objects.create(
                                enquiry_id_id = enquiry_id,
                                ec_sid = None,
                                task_id_id = 'PEACON',
                                task_assigned_to = None,
                                task_assigned_date = None,
                                task_completion_date = None
                                )  
                            else:
                                TaskManager.objects.create(
                                enquiry_id_id = enquiry_id,
                                ec_sid = None,
                                task_id_id = 'PDACON',
                                task_assigned_to = None,
                                task_assigned_date = None,
                                task_completion_date = None
                                )

                        TaskManager.objects.filter(pk=task.pk,task_id='GRDMAT').update(task_completion_date=timezone.now())
                        print('GRDNEG - CLERIC grade present and changed')
                elif EnquiryRequestParts.objects.get(cer_sid=enquiry_id).grade_confirmed_ind == 'Y':
                    #mark has changed, grade has not changed
                    TaskManager.objects.create(
                            enquiry_id_id = enquiry_id,
                            ec_sid = None,
                            task_id_id = 'COMPLT',
                            task_assigned_to = User.objects.get(username='NovaServer'),
                            task_assigned_date = timezone.now(),
                            task_completion_date = timezone.now()
                    )
                    TaskManager.objects.filter(pk=task.pk,task_id='GRDMAT').update(task_completion_date=timezone.now())
                else:
                    if task.task_creation_date + datetime.timedelta(days=7) < timezone.now():
                        clr_needed = []
                        clr_complete = []
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
                                enquiry_id_id = enquiry_id,
                                ec_sid = None,
                                task_id_id = 'COMPLT',
                                task_assigned_to = User.objects.get(username='NovaServer'),
                                task_assigned_date = timezone.now(),
                                task_completion_date = timezone.now()
                            )
                            TaskManager.objects.filter(pk=task.pk,task_id='GRDMAT').update(task_completion_date=timezone.now())                           
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
                                enquiry_id_id = enquiry_id,
                                ec_sid = None,
                                task_id_id = 'COMPLT',
                                task_assigned_to = User.objects.get(username='NovaServer'),
                                task_assigned_date = timezone.now(),
                                task_completion_date = timezone.now()
                            )
                            TaskManager.objects.filter(pk=task.pk,task_id='GRDMAT').update(task_completion_date=timezone.now())
        else:
            print('no MIS data')
            
run_algo()