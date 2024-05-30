import sys
import os
import django
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

from enquiries.models import TaskManager, EnquiryComponents, EnquiryComponentsPreviousExaminers, EnquiryPersonnelDetails, ScriptApportionment, CentreEnquiryRequests, ExaminerConflicts, ExaminerAvailability, SetIssueAudit, TaskTypes, ExaminerPanels, EnquiryComponentsExaminerChecks,EnquiryComponentsHistory
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth.models import User

def run_algo():
    start_time = datetime.datetime.now()
    print("Start Time:" + str(datetime.datetime.now()))
    chosen_script = 2058466

    for app_task in TaskManager.objects.filter(task_id='AUTAPP',ec_sid=chosen_script):
        task_pk = app_task.pk
        script_id = app_task.ec_sid.ec_sid
        task_enquiry_id = app_task.enquiry_id.enquiry_id
        script_obj = EnquiryComponents.objects.get(ec_sid=script_id)
        conflicts = ExaminerConflicts.objects.all()
        panel_manapp_flag = None
        if ExaminerPanels.objects.filter(ass_code=script_obj.eps_ass_code,com_id=script_obj.eps_com_id).exists:
            try:
                panel_manapp_flag = ExaminerPanels.objects.filter(ass_code=script_obj.eps_ass_code,com_id=script_obj.eps_com_id).first().manual_apportionment
            except:
                pass
        script_obj.eps_ass_code
        if SetIssueAudit.objects.filter(enquiry_id=task_enquiry_id).exists() or panel_manapp_flag:
            #AUTAPP not successful, send to manual apportionement - because there is an issue tagged to the enquiry or the panel is set to manual
            print('Issue or panel flag')
        else:        
            examiner_detail_obj = EnquiryPersonnelDetails.objects.filter(ass_code=script_obj.eps_ass_code,com_id=script_obj.eps_com_id,session=app_task.enquiry_id.eps_ses_sid).order_by('exm_creditor_no')
            exms_list = []
            for exm in examiner_detail_obj:
                #load examiners for this script into array
                #exm_cred, exm_pos, rank
                #r0 = Unknown, r1 = PE, r2 = TL, r3 = all others, r4 = non-viable
                exm_pos = exm.exm_examiner_no
                if exm_pos == "01.01":
                    rank = 1
                elif exm_pos[3:] == "01":
                    rank = 2
                else:
                    rank = 3

                exm_list = {'creditor':exm.exm_creditor_no, 'position':exm_pos, 'rank':rank, 'scripts':0}
                exms_list.append(exm_list)

            sorted_exms_list_rank = []
            sorted_exms_list_robin = []
            if exms_list:
                for exm in exms_list:
                    #check for previous examiners
                    prev_exm = None
                    exm_creditor_position = exm.get('position')
                    try:
                        prev_exm = EnquiryComponentsPreviousExaminers.objects.get(exm_position = exm_creditor_position, ec_sid = script_id)
                    except:
                         pass
                    if prev_exm is not None:
                        exm['rank'] = 4 #mark as non-viable

                    #check for conflicts
                    conflicts = None
                    exm_creditor_no = exm.get('creditor')
                    try:
                        conflicts = ExaminerConflicts.objects.get(creditor__exm_creditor_no = exm_creditor_no)
                    except:
                        pass
                    if conflicts is not None:
                        if script_obj.erp_sid.cer_sid.centre_id in conflicts.examiner_conflicts:
                            exm['rank'] = 4 #mark as non-viable

                    #check for unavailability
                    exm_available = True
                    current_date = timezone.now().date()
                    for ex_un_av in ExaminerAvailability.objects.filter(creditor__exm_creditor_no = exm_creditor_no):
                        start_date_minus_five = ex_un_av.unavailability_start_date - datetime.timedelta(days=5)
                        d0 = start_date_minus_five - current_date
                        d1 = ex_un_av.unavailability_end_date - current_date
                        if d0.days < 0 and d1.days > 0:
                            exm_available = False
                    if exm_available == False:
                        exm['rank'] = 4 #mark as non-viable

                    #check for script overloading
                    scripts = 0
                    scripts_qc = ScriptApportionment.objects.filter(enpe_sid__per_sid__exm_creditor_no = exm_creditor_no).all()
                    scripts_dict = scripts_qc.aggregate(Sum('script_marked'))
                    if scripts_dict['script_marked__sum'] is not None:
                        scripts = scripts_dict['script_marked__sum']

                    if scripts > 19:
                        exm['rank'] = 4 #mark as non-viable
                    exm['scripts'] = scripts

                print('All Examiners:')
                print(exms_list)
                exms_list_filtered = []
                exms_list_filtered[:] = [d for d in exms_list if d.get('rank') != 4]
                #sort final list - this is a rank order 
                sorted_exms_list_rank = sorted(exms_list_filtered, key=lambda k: (k['rank'], k['scripts'], k['position']))

                #sort final list - this is a round-robin script order 
                sorted_exms_list_robin = sorted(exms_list_filtered, key=lambda k: (k['scripts'], k['rank'], k['position']))

                print('Available Examiners:')
                print(sorted_exms_list_robin)
                
            #get "best" examiner for apportionment
            if sorted_exms_list_robin:
                chosen_exm = sorted_exms_list_robin[0]['creditor']
                print(str(script_id) + ' script id given to examiner ' + str(chosen_exm))
                print('')                
                if chosen_exm is not None:
                    if EnquiryComponents.objects.get(ec_sid=script_id).erp_sid.service_code == '3':
                        print('Service 3')
                    else:
                        if EnquiryComponents.objects.get(ec_sid=script_id).script_type == "RM Assessor":
                            print('RM Assessor')
                        else:
                            print('Hardcopy')
                else:
                    #AUTAPP not successful, send to manual apportionement
                    print('Manual: No examiner late')         
            else:
                #AUTAPP not successful, send to manual apportionement - because no examiners in panel
                print('Manual: No examiner early') 



    end_time = datetime.datetime.now()
    print(end_time - start_time)      

run_algo()