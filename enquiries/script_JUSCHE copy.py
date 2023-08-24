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
        print(task.ec_sid.erp_sid.cer_sid.enquiry_id)
        mis_data = MisReturnData.objects.filter(ec_sid=task.ec_sid.ec_sid).first()
        
        print(mis_data)
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
                    is_scaled_exm = scaled_mark_set.original_exm_scaled == 'Scaled'
                    within_tolerance = int(abs(int(final_mark)-scaled_mark)) <= int(mark_tolerance)

                if len(justification_string.strip()) == 1:
                    final_justification_code = justification_string
                
                if justification_string.find('5') != -1 and justification_string.find('6') != -1:
                    if within_tolerance:
                        final_justification_code = 5
                    else:
                        final_justification_code = 6
                
                if justification_string.find('5') != -1 and justification_string.find('7') != -1:
                    if within_tolerance and is_scaled_exm:
                        final_justification_code = 7
                    elif within_tolerance and not is_scaled_exm:
                        final_justification_code = 5 

                if justification_string.find('5') != -1 and justification_string.find('8') != -1:
                    if not within_tolerance and is_scaled_exm:
                        final_justification_code = 8
                    elif within_tolerance and not is_scaled_exm:
                        final_justification_code = 5                                 

                if justification_string.find('6') != -1 and justification_string.find('7') != -1:
                    if not within_tolerance:
                        final_justification_code = 6
                    elif within_tolerance and is_scaled_exm:
                        final_justification_code = 7 

                if justification_string.find('6') != -1 and justification_string.find('8') != -1:
                    if not within_tolerance and not is_scaled_exm:
                        final_justification_code = 6
                    elif not within_tolerance and is_scaled_exm:
                        final_justification_code = 8 

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

                # if final_justification_code == 5 and 

                # mis_data.selected_justification_code = final_justification_code
                # mis_data.keying_required = 'Y'
                # mis_data.keyed_mark_status = 'Changed'
                # mis_data.save() 



            # *Apply key/no key rules to justification codes;
            # *check if 5 within tolerance;
            # else if FinalJustification='5' then do;
            #   if WithinTolerance='YES' then For_office_use='NK 5';
            #   else query='Query - Tolerance';
            # end;
            # *check if 6 outside tolerance and not marked by PE;
            # else if FinalJustification='6' then do;
            #   if WithinTolerance='NO' then do;
            #     For_office_use='K 6';
            #   end;
            #   else query='Query - Tolerance';
            # end;
            # *check if 7 within tolerance, query if examiner was not scaled or scaling not known;
            # else if FinalJustification='7' then do;
            #   if WithinTolerance='YES' then do;
            #     For_office_use='NK 7';
            #     if origexmrscaled in ('No scaling' 'Original mark not found') then query='Query - Scaling';
            #   end;
            #   else query='Query - Tolerance';
            # end;
            # *check if 8 outside tolerance, query if examiner was not scaled or scaling not known;
            # else if FinalJustification='8' then do;
            #   if WithinTolerance='NO' then do;
            #     For_office_use='K 8';
            #     if origexmrscaled in ('No scaling' 'Original mark not found') then query='Query - Scaling';
            #   end;
            #   else query='Query - Tolerance';
            # end;
   

run_algo()