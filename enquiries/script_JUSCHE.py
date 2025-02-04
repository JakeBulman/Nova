import sys
import os
import django
from django.utils import timezone
import datetime, re

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

from enquiries.models import TaskManager, EnquiryComponents, CentreEnquiryRequests, MisReturnData, TaskTypes, MarkTolerances, ScaledMarks, EnquiryComponentsExaminerChecks, EnquiryComponentsHistory
from django.contrib.auth.models import User

def return_int(possible_int):
    try:
        int(possible_int)
        return possible_int
    except:
        pass
        return None

def run_algo():
    for task in TaskManager.objects.filter(task_id='JUSCHE', task_completion_date__isnull=True):
        print(task.ec_sid.ec_sid)

        if not MisReturnData.objects.filter(ec_sid=task.ec_sid.ec_sid).exists():
            print("MIS Data Missing")
            TaskManager.objects.create(
                enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task.enquiry_id.enquiry_id),
                ec_sid = EnquiryComponents.objects.get(ec_sid=task.ec_sid.ec_sid),
                task_id = TaskTypes.objects.get(task_id = 'MISVRF'),
                task_assigned_to = None,
                task_assigned_date = None,
                task_completion_date = None
            )
            TaskManager.objects.filter(pk=task.pk,task_id='JUSCHE').update(task_completion_date=timezone.now())  
            continue
        else:
            mis_data = MisReturnData.objects.filter(ec_sid=task.ec_sid.ec_sid).first()
            justification_string = re.sub("[^0-9]", "", str(mis_data.final_justification_code))
            final_mark_status = mis_data.final_mark_status
            final_mark = mis_data.final_mark
            original_mark = mis_data.original_mark

        #Check for bad statuses
        if final_mark_status not in ['Confirmed','Changed']:
            print('NO STATUS')
            mis_data.error_status = "No status"
            mis_data.save()
            TaskManager.objects.create(
                enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task.enquiry_id.enquiry_id),
                ec_sid = EnquiryComponents.objects.get(ec_sid=task.ec_sid.ec_sid),
                task_id = TaskTypes.objects.get(task_id = 'MISVRF'),
                task_assigned_to = None,
                task_assigned_date = None,
                task_completion_date = None
            )
            TaskManager.objects.filter(pk=task.pk,task_id='JUSCHE').update(task_completion_date=timezone.now())  
            continue
        if final_mark_status == 'Changed' and (justification_string is None or justification_string.strip() == '' or final_mark is None):
            print('NO JC or Mark')
            mis_data.error_status = "No JC or Mark"
            mis_data.save()
            TaskManager.objects.create(
                enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task.enquiry_id.enquiry_id),
                ec_sid = EnquiryComponents.objects.get(ec_sid=task.ec_sid.ec_sid),
                task_id = TaskTypes.objects.get(task_id = 'MISVRF'),
                task_assigned_to = None,
                task_assigned_date = None,
                task_completion_date = None
            )
            TaskManager.objects.filter(pk=task.pk,task_id='JUSCHE').update(task_completion_date=timezone.now())  
            continue
            #New for N24, check if mark is confirmed but mark present
        try:
            if final_mark_status == 'Confirmed' and ((justification_string is not None and justification_string != '') or (final_mark is not None and final_mark != 'None')) and (int(final_mark) != int(float(original_mark))):
                print(final_mark)
                print(original_mark)
                print('Confirmed, with JC or Mark')
                mis_data.error_status = "Confirmed, with JC or Mark"
                mis_data.save()
                TaskManager.objects.create(
                    enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task.enquiry_id.enquiry_id),
                    ec_sid = EnquiryComponents.objects.get(ec_sid=task.ec_sid.ec_sid),
                    task_id = TaskTypes.objects.get(task_id = 'MISVRF'),
                    task_assigned_to = None,
                    task_assigned_date = None,
                    task_completion_date = None
                )
                TaskManager.objects.filter(pk=task.pk,task_id='JUSCHE').update(task_completion_date=timezone.now())  
                continue
        except:
            pass
            mis_data.error_status = "MIS Configuration issue"
            mis_data.save()
            TaskManager.objects.create(
                enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task.enquiry_id.enquiry_id),
                ec_sid = EnquiryComponents.objects.get(ec_sid=task.ec_sid.ec_sid),
                task_id = TaskTypes.objects.get(task_id = 'MISVRF'),
                task_assigned_to = None,
                task_assigned_date = None,
                task_completion_date = None
            )
            TaskManager.objects.filter(pk=task.pk,task_id='JUSCHE').update(task_completion_date=timezone.now())  
            continue
        

        #Check MIS has scaling applied
        if not MarkTolerances.objects.filter(eps_ass_code=task.ec_sid.eps_ass_code, eps_com_id=task.ec_sid.eps_com_id).exists():
            print("Tolerance Not Available")
            mis_data.error_status = "Tolerance Not Available"
            mis_data.save()
            TaskManager.objects.create(
                enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task.enquiry_id.enquiry_id),
                ec_sid = EnquiryComponents.objects.get(ec_sid=task.ec_sid.ec_sid),
                task_id = TaskTypes.objects.get(task_id = 'MISVRF'),
                task_assigned_to = None,
                task_assigned_date = None,
                task_completion_date = None
            )
            TaskManager.objects.filter(pk=task.pk,task_id='JUSCHE').update(task_completion_date=timezone.now())  
            continue
        else:
            early_mark_tolerance = MarkTolerances.objects.filter(eps_ass_code=task.ec_sid.eps_ass_code, eps_com_id=task.ec_sid.eps_com_id).first().mark_tolerance

        if not ScaledMarks.objects.filter(eps_ass_code=task.ec_sid.eps_ass_code, eps_com_id=task.ec_sid.eps_com_id, eps_cnu_id=task.ec_sid.erp_sid.eps_centre_id, eps_cand_no=task.ec_sid.erp_sid.eps_cand_id,eps_ses_sid=task.ec_sid.eps_ses_sid).exists():
            print("No scaled mark available - see JB")
            mis_data.error_status = "No mark available"
            mis_data.save()
            TaskManager.objects.create(
                enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task.enquiry_id.enquiry_id),
                ec_sid = EnquiryComponents.objects.get(ec_sid=task.ec_sid.ec_sid),
                task_id = TaskTypes.objects.get(task_id = 'MISVRF'),
                task_assigned_to = None,
                task_assigned_date = None,
                task_completion_date = None
            )
            TaskManager.objects.filter(pk=task.pk,task_id='JUSCHE').update(task_completion_date=timezone.now())  
            continue
        else:
            scaled_mark_set = ScaledMarks.objects.filter(eps_ass_code=task.ec_sid.eps_ass_code, eps_com_id=task.ec_sid.eps_com_id, eps_cnu_id=task.ec_sid.erp_sid.eps_centre_id, eps_cand_no=task.ec_sid.erp_sid.eps_cand_id,eps_ses_sid=task.ec_sid.eps_ses_sid).first()
            print(mis_data.original_mark)
            scaled_mark = int(scaled_mark_set.scaled_mark.split('.')[0])
            try:
                mis_mark = int(mis_data.original_mark.split('.')[0])
            except:
                mis_mark = 0
            print(str(scaled_mark) + " " + str(mis_mark))
            scaled_mark_on_mis = str(scaled_mark) == str(mis_mark)
            print(scaled_mark_on_mis)
            within_tolerance = int(abs(int(mis_mark)-scaled_mark)) <= int(early_mark_tolerance)
            print(within_tolerance)

    


        if final_mark_status == 'Confirmed':
            print('CONF')
            if not scaled_mark_on_mis and within_tolerance:
                print('Conf InTol needs checking')
                mis_data.error_status = "Conf InTol needs checking"
                mis_data.save()
                TaskManager.objects.create(
                    enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task.enquiry_id.enquiry_id),
                    ec_sid = EnquiryComponents.objects.get(ec_sid=task.ec_sid.ec_sid),
                    task_id = TaskTypes.objects.get(task_id = 'MISVRF'),
                    task_assigned_to = None,
                    task_assigned_date = None,
                    task_completion_date = None
                )
                TaskManager.objects.filter(pk=task.pk,task_id='JUSCHE').update(task_completion_date=timezone.now())  
                continue
            
            elif not scaled_mark_on_mis and not within_tolerance:
                print('Conf OutTol')
                final_justification_code = 8
                final_keying_required = 'Y'
                final_keyed_mark_status = 'Changed' 
                mis_data.selected_justification_code = final_justification_code
                mis_data.keying_required = final_keying_required
                mis_data.keyed_mark_status = final_keyed_mark_status
                mis_data.final_mark = mis_data.original_mark
                mis_data.save() 

                print(final_justification_code)
                print(final_keying_required)
                print(final_keyed_mark_status)  
            else:
                print('Conf NoScale')
                mis_data.keyed_mark_status = 'Confirmed'
                mis_data.keying_required = 'Y'
                mis_data.save()
            kbr_code = EnquiryComponentsHistory.objects.get(ec_sid=task.ec_sid.ec_sid).kbr_code
            print(kbr_code)
            if kbr_code in ('AM','AWGE','AWGF','AWGP','AWGR','EXMF','EXMP','EXMR','MP','PBD','PGR','REG','SC'):
                TaskManager.objects.create(
                    enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task.enquiry_id.enquiry_id),
                    ec_sid = EnquiryComponents.objects.get(ec_sid=task.ec_sid.ec_sid),
                    task_id = TaskTypes.objects.get(task_id = 'MARCHE'),
                    task_assigned_to = User.objects.get(username='NovaServer'),
                    task_assigned_date = timezone.now(),
                    task_completion_date = None
                )    
            else:
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
                kbr_code = EnquiryComponentsHistory.objects.get(ec_sid=task.ec_sid.ec_sid).kbr_code
                print(kbr_code)
                if kbr_code in ('AM','AWGE','AWGF','AWGP','AWGR','EXMF','EXMP','EXMR','MP','PBD','PGR','REG','SC'):
                    TaskManager.objects.create(
                        enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task.enquiry_id.enquiry_id),
                        ec_sid = EnquiryComponents.objects.get(ec_sid=task.ec_sid.ec_sid),
                        task_id = TaskTypes.objects.get(task_id = 'MARCHE'),
                        task_assigned_to = User.objects.get(username='NovaServer'),
                        task_assigned_date = timezone.now(),
                        task_completion_date = None
                    )    
                else:
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
                kbr_code = EnquiryComponentsHistory.objects.get(ec_sid=task.ec_sid.ec_sid).kbr_code
                print(kbr_code)
                if kbr_code in ('AM','AWGE','AWGF','AWGP','AWGR','EXMF','EXMP','EXMR','MP','PBD','PGR','REG','SC'):
                    TaskManager.objects.create(
                        enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task.enquiry_id.enquiry_id),
                        ec_sid = EnquiryComponents.objects.get(ec_sid=task.ec_sid.ec_sid),
                        task_id = TaskTypes.objects.get(task_id = 'MARCHE'),
                        task_assigned_to = User.objects.get(username='NovaServer'),
                        task_assigned_date = timezone.now(),
                        task_completion_date = None
                    )    
                else:
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
                kbr_code = EnquiryComponentsHistory.objects.get(ec_sid=task.ec_sid.ec_sid).kbr_code
                print(kbr_code)
                if kbr_code in ('AM','AWGE','AWGF','AWGP','AWGR','EXMF','EXMP','EXMR','MP','PBD','PGR','REG','SC'):
                    TaskManager.objects.create(
                        enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task.enquiry_id.enquiry_id),
                        ec_sid = EnquiryComponents.objects.get(ec_sid=task.ec_sid.ec_sid),
                        task_id = TaskTypes.objects.get(task_id = 'MARCHE'),
                        task_assigned_to = User.objects.get(username='NovaServer'),
                        task_assigned_date = timezone.now(),
                        task_completion_date = None
                    )    
                else:
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
                kbr_code = EnquiryComponentsHistory.objects.get(ec_sid=task.ec_sid.ec_sid).kbr_code
                print(kbr_code)
                if kbr_code in ('AM','AWGE','AWGF','AWGP','AWGR','EXMF','EXMP','EXMR','MP','PBD','PGR','REG','SC'):
                    TaskManager.objects.create(
                        enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task.enquiry_id.enquiry_id),
                        ec_sid = EnquiryComponents.objects.get(ec_sid=task.ec_sid.ec_sid),
                        task_id = TaskTypes.objects.get(task_id = 'MARCHE'),
                        task_assigned_to = User.objects.get(username='NovaServer'),
                        task_assigned_date = timezone.now(),
                        task_completion_date = None
                    )    
                else:
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

                if not ScaledMarks.objects.filter(eps_ass_code=task.ec_sid.eps_ass_code, eps_com_id=task.ec_sid.eps_com_id, eps_cnu_id=task.ec_sid.erp_sid.eps_centre_id, eps_cand_no=task.ec_sid.erp_sid.eps_cand_id,eps_ses_sid=task.ec_sid.eps_ses_sid).exists():
                    print("No scaled mark available")
                else:
                    scaled_mark_set = ScaledMarks.objects.filter(eps_ass_code=task.ec_sid.eps_ass_code, eps_com_id=task.ec_sid.eps_com_id, eps_cnu_id=task.ec_sid.erp_sid.eps_centre_id, eps_cand_no=task.ec_sid.erp_sid.eps_cand_id,eps_ses_sid=task.ec_sid.eps_ses_sid).first()
                    scaled_mark = int(scaled_mark_set.scaled_mark.split('.')[0])
                    print(final_mark)
                    try:
                        final_mark = int(final_mark.split('.')[0])
                    except:
                        print("MIS Mark Bad Input")
                        mis_data.error_status = "MIS Mark Bad Input"
                        mis_data.save()
                        TaskManager.objects.create(
                            enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task.enquiry_id.enquiry_id),
                            ec_sid = EnquiryComponents.objects.get(ec_sid=task.ec_sid.ec_sid),
                            task_id = TaskTypes.objects.get(task_id = 'MISVRF'),
                            task_assigned_to = None,
                            task_assigned_date = None,
                            task_completion_date = None
                        )
                        TaskManager.objects.filter(pk=task.pk,task_id='JUSCHE').update(task_completion_date=timezone.now())  
                        continue
                    is_scaled_exm = scaled_mark_set.original_exm_scaled == 'Scaled'
                    within_tolerance = int(abs(int(final_mark)-scaled_mark)) <= int(mark_tolerance)

                final_justification_code = None
                justification_string = justification_string.replace('0','')
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

                print(final_justification_code)
                if int(final_justification_code) == 7 and not is_scaled_exm: final_justification_code = 5
                if int(final_justification_code) == 8 and not is_scaled_exm: final_justification_code = 6
                if int(final_justification_code) == 5 and is_scaled_exm: final_justification_code = 7
                if int(final_justification_code) == 6 and is_scaled_exm: final_justification_code = 8

                if EnquiryComponentsExaminerChecks.objects.filter(ec_sid = task.ec_sid.ec_sid).count() > 0:
                    print("Prev exm check")
                    if int(final_justification_code) == 7: final_justification_code = 5
                    if int(final_justification_code) == 8: final_justification_code = 6


                if final_justification_code is None:
                    print("No JC - 5678")
                    mis_data.error_status = "No JC - 5678"
                    mis_data.save()
                    TaskManager.objects.create(
                        enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task.enquiry_id.enquiry_id),
                        ec_sid = EnquiryComponents.objects.get(ec_sid=task.ec_sid.ec_sid),
                        task_id = TaskTypes.objects.get(task_id = 'MISVRF'),
                        task_assigned_to = None,
                        task_assigned_date = None,
                        task_completion_date = None
                    )
                    TaskManager.objects.filter(pk=task.pk,task_id='JUSCHE').update(task_completion_date=timezone.now())  
                    continue

                print(final_justification_code)
                print('TOL:' + str(within_tolerance))
                print('SCALE:' + str(is_scaled_exm))
                print(task.ec_sid.ec_sid)

                if int(final_justification_code) == 5: 
                    if within_tolerance:
                        final_keying_required = 'N'
                        final_keyed_mark_status = 'Confirmed'
                    else:
                        final_justification_code = 6
                        final_keying_required = 'Y'
                        final_keyed_mark_status = 'Changed'

                if int(final_justification_code) == 6: 
                    if not within_tolerance:
                        final_keying_required = 'Y'
                        final_keyed_mark_status = 'Changed'
                    else:
                        final_justification_code = 5
                        final_keying_required = 'N'
                        final_keyed_mark_status = 'Confirmed'

                if int(final_justification_code) == 7: 
                    if within_tolerance:
                        final_keying_required = 'N'
                        final_keyed_mark_status = 'Confirmed'
                    else:
                        final_justification_code = 8
                        final_keying_required = 'Y'
                        final_keyed_mark_status = 'Changed'

                if int(final_justification_code) == 8: 
                    if not within_tolerance:
                        final_keying_required = 'Y'
                        final_keyed_mark_status = 'Changed'
                    else:
                        final_justification_code = 7
                        final_keying_required = 'N'
                        final_keyed_mark_status = 'Confirmed'

                mis_data.selected_justification_code = final_justification_code
                mis_data.keying_required = final_keying_required
                mis_data.keyed_mark_status = final_keyed_mark_status
                mis_data.save() 

                print(final_justification_code)
                print(final_keying_required)
                print(final_keyed_mark_status)
                kbr_code = EnquiryComponentsHistory.objects.get(ec_sid=task.ec_sid.ec_sid).kbr_code
                print(kbr_code)
                if kbr_code in ('AM','AWGE','AWGF','AWGP','AWGR','EXMF','EXMP','EXMR','MP','PBD','PGR','REG','SC'):
                    TaskManager.objects.create(
                        enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task.enquiry_id.enquiry_id),
                        ec_sid = EnquiryComponents.objects.get(ec_sid=task.ec_sid.ec_sid),
                        task_id = TaskTypes.objects.get(task_id = 'MARCHE'),
                        task_assigned_to = None,
                        task_assigned_date = None,
                        task_completion_date = None
                    )    
                else:
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