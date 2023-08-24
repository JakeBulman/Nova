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

from enquiries.models import TaskManager, EnquiryComponents, CentreEnquiryRequests, MisReturnData, TaskTypes, MarkTolerances, ScaledMarks, EnquiryComponentsExaminerChecks
from django.contrib.auth.models import User

def run_algo():
    for task in TaskManager.objects.filter(task_id='JUSCHE', task_completion_date__isnull=True):

        mis_data = MisReturnData.objects.filter(ec_sid=task.ec_sid.ec_sid).first()
        justification_string = mis_data.final_justification_code
        final_mark_status = mis_data.final_mark_status
        final_mark = mis_data.final_mark
        # If confirmed, pass straight through
        if final_mark_status not in ['Confirmed','Changed']:
            print('NO STATUS')
            continue
        if final_mark_status == 'Changed' and (justification_string is None or final_mark is None):
            print('NO JC or Mark')
            continue

        if final_mark_status == 'Confirmed':
            mis_data.keyed_mark_status = 'Confirmed'
            mis_data.keying_required = 'Y'
            mis_data.save()
            TaskManager.objects.create(
                enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task.enquiry_id.enquiry_id),
                ec_sid = EnquiryComponents.objects.get(ec_sid=task.ec_sid.ec_sid),
                task_id = TaskTypes.objects.get(task_id = 'MKWAIT'),
                task_assigned_to = User.objects.get(username='NovaServer'),
                task_assigned_date = timezone.now(),
                task_completion_date = None
            )
            TaskManager.objects.filter(pk=task.pk,task_id='JUSCHE').update(task_completion_date=timezone.now())   

        else:  
            # each of the codes 1-4 even if other things present
            # order is 4, 2, 3, 1 
            print("JC=" + justification_string)
            if justification_string.find('4') != -1:
                mis_data.selected_justification_code = '4'
                mis_data.keying_required = 'Y'
                mis_data.keyed_mark_status = 'Changed'
                mis_data.save() 
                print(4)
                TaskManager.objects.create(
                    enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task.enquiry_id.enquiry_id),
                    ec_sid = EnquiryComponents.objects.get(ec_sid=task.ec_sid.ec_sid),
                    task_id = TaskTypes.objects.get(task_id = 'MKWAIT'),
                    task_assigned_to = User.objects.get(username='NovaServer'),
                    task_assigned_date = timezone.now(),
                    task_completion_date = None
                )
                TaskManager.objects.filter(pk=task.pk,task_id='JUSCHE').update(task_completion_date=timezone.now())   

            elif justification_string.find('2') != -1:
                mis_data.selected_justification_code = '2'
                mis_data.keying_required = 'Y'
                mis_data.keyed_mark_status = 'Changed'
                mis_data.save() 
                print(2)

                TaskManager.objects.create(
                    enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task.enquiry_id.enquiry_id),
                    ec_sid = EnquiryComponents.objects.get(ec_sid=task.ec_sid.ec_sid),
                    task_id = TaskTypes.objects.get(task_id = 'MKWAIT'),
                    task_assigned_to = User.objects.get(username='NovaServer'),
                    task_assigned_date = timezone.now(),
                    task_completion_date = None
                )
                TaskManager.objects.filter(pk=task.pk,task_id='JUSCHE').update(task_completion_date=timezone.now())   

            elif justification_string.find('3') != -1:
                mis_data.selected_justification_code = '3'
                mis_data.keying_required = 'Y'
                mis_data.keyed_mark_status = 'Changed'
                mis_data.save()
                print(3) 
                TaskManager.objects.create(
                    enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task.enquiry_id.enquiry_id),
                    ec_sid = EnquiryComponents.objects.get(ec_sid=task.ec_sid.ec_sid),
                    task_id = TaskTypes.objects.get(task_id = 'MKWAIT'),
                    task_assigned_to = User.objects.get(username='NovaServer'),
                    task_assigned_date = timezone.now(),
                    task_completion_date = None
                )
                TaskManager.objects.filter(pk=task.pk,task_id='JUSCHE').update(task_completion_date=timezone.now())   

            elif justification_string.find('1') != -1:
                mis_data.selected_justification_code = '1'
                mis_data.keying_required = 'Y'
                mis_data.keyed_mark_status = 'Changed'
                mis_data.save() 
                print(1)
                TaskManager.objects.create(
                    enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task.enquiry_id.enquiry_id),
                    ec_sid = EnquiryComponents.objects.get(ec_sid=task.ec_sid.ec_sid),
                    task_id = TaskTypes.objects.get(task_id = 'MKWAIT'),
                    task_assigned_to = User.objects.get(username='NovaServer'),
                    task_assigned_date = timezone.now(),
                    task_completion_date = None
                )
                TaskManager.objects.filter(pk=task.pk,task_id='JUSCHE').update(task_completion_date=timezone.now())  

            else:

                if not MarkTolerances.objects.filter(eps_ass_code=task.ec_sid.eps_ass_code, eps_com_id=task.ec_sid.eps_com_id).exists():
                    print("Tolerance Not Available")
                else:
                    mark_tolerance = MarkTolerances.objects.filter(eps_ass_code=task.ec_sid.eps_ass_code, eps_com_id=task.ec_sid.eps_com_id).first().mark_tolerance

                if not ScaledMarks.objects.filter(eps_ass_code=task.ec_sid.eps_ass_code, eps_com_id=task.ec_sid.eps_com_id, eps_cnu_id=task.ec_sid.erp_sid.eps_centre_id, eps_cand_no=task.ec_sid.erp_sid.eps_cand_id).exists():
                    print("No mark available")
                else:
                    scaled_mark_set = ScaledMarks.objects.filter(eps_ass_code=task.ec_sid.eps_ass_code, eps_com_id=task.ec_sid.eps_com_id, eps_cnu_id=task.ec_sid.erp_sid.eps_centre_id, eps_cand_no=task.ec_sid.erp_sid.eps_cand_id).first()
                    scaled_mark = int(scaled_mark_set.scaled_mark.split('.')[0])
                    is_scaled_exm = scaled_mark_set.original_exm_scaled == 'Scaled'
                    within_tolerance = int(abs(int(final_mark)-scaled_mark)) <= int(mark_tolerance)

                if len(justification_string.strip()) == 1:
                    final_justification_code = justification_string.strip()
                    final_keying_required = 'Y'
                    final_keyed_mark_status = 'Changed'                    
                
                if justification_string.find('5') != -1 and justification_string.find('6') != -1:
                    if within_tolerance:
                        final_justification_code = 5
                        final_keying_required = 'Y'
                        final_keyed_mark_status = 'Changed' 
                    else:
                        final_justification_code = 6
                        final_keying_required = 'Y'
                        final_keyed_mark_status = 'Changed' 
                
                if justification_string.find('5') != -1 and justification_string.find('7') != -1:
                    if within_tolerance and is_scaled_exm:
                        final_justification_code = 7
                        final_keying_required = 'Y'
                        final_keyed_mark_status = 'Changed'                         
                    elif within_tolerance and not is_scaled_exm:
                        final_justification_code = 5 
                        final_keying_required = 'Y'
                        final_keyed_mark_status = 'Changed'                         

                if justification_string.find('5') != -1 and justification_string.find('8') != -1:
                    if not within_tolerance and is_scaled_exm:
                        final_justification_code = 8
                        final_keying_required = 'Y'
                        final_keyed_mark_status = 'Changed'                         
                    elif within_tolerance and not is_scaled_exm:
                        final_justification_code = 5  
                        final_keying_required = 'Y'
                        final_keyed_mark_status = 'Changed'                                                        

                if justification_string.find('6') != -1 and justification_string.find('7') != -1:
                    if not within_tolerance:
                        final_justification_code = 6
                        final_keying_required = 'Y'
                        final_keyed_mark_status = 'Changed'  
                    elif within_tolerance and is_scaled_exm:
                        final_justification_code = 7 
                        final_keying_required = 'Y'
                        final_keyed_mark_status = 'Changed'  

                if justification_string.find('6') != -1 and justification_string.find('8') != -1:
                    if not within_tolerance and not is_scaled_exm:
                        final_justification_code = 6
                        final_keying_required = 'Y'
                        final_keyed_mark_status = 'Changed'  
                    elif not within_tolerance and is_scaled_exm:
                        final_justification_code = 8 
                        final_keying_required = 'Y'
                        final_keyed_mark_status = 'Changed'  

                if final_justification_code == 7 and not is_scaled_exm: final_justification_code = 5
                if final_justification_code == 8 and not is_scaled_exm: final_justification_code = 6
                if final_justification_code == 5 and is_scaled_exm: final_justification_code = 7
                if final_justification_code == 6 and is_scaled_exm: final_justification_code = 8

                if EnquiryComponentsExaminerChecks.objects.filter(ec_sid = task.ec_sid.ec_sid).count() > 0:
                    print("Prev exm check")
                    if final_justification_code == 7: final_justification_code = 5
                    if final_justification_code == 8: final_justification_code = 6


                if final_justification_code is None:
                    print("No JC - 5678")

                print(final_justification_code)

                if final_justification_code == 5: 
                    if within_tolerance:
                        final_keying_required = 'N'
                        final_keyed_mark_status = 'Confirmed'
                    else:
                        print('JC5 Tolerance')
                        continue

                if final_justification_code == 6: 
                    if not within_tolerance:
                        final_keying_required = 'Y'
                        final_keyed_mark_status = 'Changed'
                    else:
                        print('JC6 Tolerance')
                        continue

                if final_justification_code == 7: 
                    if within_tolerance:
                        final_keying_required = 'N'
                        final_keyed_mark_status = 'Confirmed'
                    else:
                        print('JC7 Tolerance')
                        continue

                if final_justification_code == 8: 
                    if not within_tolerance:
                        final_keying_required = 'N'
                        final_keyed_mark_status = 'Confirmed'
                    else:
                        print('JC8 Tolerance')
                        continue

                mis_data.selected_justification_code = final_justification_code
                mis_data.keying_required = final_keying_required
                mis_data.keyed_mark_status = final_keyed_mark_status
                mis_data.save() 

                print(final_justification_code)
                print(final_keying_required)
                print(final_keyed_mark_status)

                TaskManager.objects.create(
                    enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task.enquiry_id.enquiry_id),
                    ec_sid = EnquiryComponents.objects.get(ec_sid=task.ec_sid.ec_sid),
                    task_id = TaskTypes.objects.get(task_id = 'MKWAIT'),
                    task_assigned_to = User.objects.get(username='NovaServer'),
                    task_assigned_date = timezone.now(),
                    task_completion_date = None
                )
                TaskManager.objects.filter(pk=task.pk,task_id='JUSCHE').update(task_completion_date=timezone.now())  


run_algo()