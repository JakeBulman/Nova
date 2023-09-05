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
    for task in TaskManager.objects.filter(task_id='JUSCHE'):
        print(task.ec_sid.ec_sid)

        if not MisReturnData.objects.filter(ec_sid=task.ec_sid.ec_sid).exists():
            print("MIS Data Missing")
            continue
        else:
            mis_data = MisReturnData.objects.filter(ec_sid=task.ec_sid.ec_sid).first()
            justification_string = mis_data.final_justification_code
            final_mark_status = mis_data.final_mark_status
            final_mark = mis_data.final_mark
        

        #Check MIS has scaling applied
        if not MarkTolerances.objects.filter(eps_ass_code=task.ec_sid.eps_ass_code, eps_com_id=task.ec_sid.eps_com_id).exists():
            print("Tolerance Not Available")
            mis_data.error_status = "Tolerance Not Available"
            mis_data.save()
            continue
        else:
            early_mark_tolerance = MarkTolerances.objects.filter(eps_ass_code=task.ec_sid.eps_ass_code, eps_com_id=task.ec_sid.eps_com_id).first().mark_tolerance

        if not ScaledMarks.objects.filter(eps_ass_code=task.ec_sid.eps_ass_code, eps_com_id=task.ec_sid.eps_com_id, eps_cnu_id=task.ec_sid.erp_sid.eps_centre_id, eps_cand_no=task.ec_sid.erp_sid.eps_cand_id).exists():
            print("No mark available")
            mis_data.error_status = "No mark available"
            mis_data.save()
            continue
        else:
            scaled_mark_set = ScaledMarks.objects.filter(eps_ass_code=task.ec_sid.eps_ass_code, eps_com_id=task.ec_sid.eps_com_id, eps_cnu_id=task.ec_sid.erp_sid.eps_centre_id, eps_cand_no=task.ec_sid.erp_sid.eps_cand_id).first()
            scaled_mark = int(scaled_mark_set.scaled_mark.split('.')[0])
            mis_mark = mis_data.original_mark
            print(str(scaled_mark) + " " + str(mis_mark))
            scaled_mark_on_mis = str(scaled_mark) == str(mis_mark)
            print(scaled_mark_on_mis)
            within_tolerance = int(abs(int(mis_mark)-scaled_mark)) <= int(early_mark_tolerance)
            print(within_tolerance)

    
        #Check for bad statuses
        if final_mark_status not in ['Confirmed','Changed']:
            print('NO STATUS')
            mis_data.error_status = "No status"
            mis_data.save()
            continue
        if final_mark_status == 'Changed' and (justification_string is None or final_mark is None):
            print('NO JC or Mark')
            mis_data.error_status = "No JC or Mark"
            mis_data.save()
            continue

        if final_mark_status == 'Confirmed':
            print('CONF')
            if not scaled_mark_on_mis and within_tolerance:
                print('Conf InTol needs checking')
                mis_data.error_status = "Conf InTol needs checking"
                mis_data.save()
                continue
            
            elif not scaled_mark_on_mis and not within_tolerance:
                print('Conf OutTol')
                final_justification_code = 8
                final_keying_required = 'Y'
                final_keyed_mark_status = 'Changed' 
                mis_data.selected_justification_code = final_justification_code
                mis_data.keying_required = final_keying_required
                mis_data.keyed_mark_status = final_keyed_mark_status
                mis_data.save() 

                print(final_justification_code)
                print(final_keying_required)
                print(final_keyed_mark_status)  
            else:
                print('Conf NoScale')
                mis_data.keyed_mark_status = 'Confirmed'
                mis_data.keying_required = 'Y'
                mis_data.save()
  

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


            elif justification_string.find('2') != -1:
                mis_data.selected_justification_code = '2'
                mis_data.keying_required = 'Y'
                mis_data.keyed_mark_status = 'Changed'
                mis_data.save() 
                print(2)



            elif justification_string.find('3') != -1:
                mis_data.selected_justification_code = '3'
                mis_data.keying_required = 'Y'
                mis_data.keyed_mark_status = 'Changed'
                mis_data.save()
                print(3) 


            elif justification_string.find('1') != -1:
                mis_data.selected_justification_code = '1'
                mis_data.keying_required = 'Y'
                mis_data.keyed_mark_status = 'Changed'
                mis_data.save() 
                print(1)


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
                    final_mark = int(final_mark.split('.')[0])
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



run_algo()