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

from enquiries.models import TaskManager, EnquiryComponents, EnquiryComponentsPreviousExaminers, EnquiryPersonnelDetails, ScriptApportionment, CentreEnquiryRequests, ExaminerConflicts, ExaminerAvailability, SetIssueAudit, TaskTypes, ExaminerPanels, EnquiryComponentsExaminerChecks,EnquiryComponentsHistory, EarServerSettings
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth.models import User

# Create your views here.
def run_algo():
    start_time = datetime.datetime.now()
    print("Start Time:" + str(datetime.datetime.now()))


    for app_task in TaskManager.objects.filter(task_id='AUTAPP', task_completion_date__isnull=True, ec_sid__script_id__eb_sid__created_date__isnull=False):
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
            TaskManager.objects.create(
                enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task_enquiry_id),
                ec_sid = EnquiryComponents.objects.get(ec_sid=script_id),
                task_id = TaskTypes.objects.get(task_id = 'MANAPP'),
                task_assigned_to = None,
                task_assigned_date = None,
                task_completion_date = None
            )      
        else:        
            examiner_detail_obj = EnquiryPersonnelDetails.objects.filter(ass_code=script_obj.eps_ass_code,com_id=script_obj.eps_com_id,session=app_task.enquiry_id.eps_ses_sid,enpe_sid__currently_valid=True).order_by('exm_creditor_no')
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
            print("exms_list:")
            print(exms_list)
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

                    #count scripts the exmanier has in all panels
                    scripts = 0
                    scripts_qc = ScriptApportionment.objects.filter(enpe_sid__per_sid__exm_creditor_no = exm_creditor_no).all()
                    scripts_dict = scripts_qc.aggregate(Sum('script_marked')) #this is filtering onto only scripts examiner has in-hand
                    if scripts_dict['script_marked__sum'] is not None:
                        scripts = scripts_dict['script_marked__sum']

                    #check for script overloading
                    if scripts > 19:
                        exm['rank'] = 4 #mark as non-viable
                    #N24 Approved change to multiply non-PE script count by 2 to provide more scripts to PE on approx 2:1 ratio (must come after "20 scripts" check)
                    if exm['position'] != "01.01":
                        exm['scripts'] = scripts * 2
                    else:
                        exm['scripts'] = scripts

                print(exms_list)
                exms_list_filtered = []
                exms_list_filtered[:] = [d for d in exms_list if d.get('rank') != 4]
                #sort final list - this is a rank order 
                sorted_exms_list_rank = sorted(exms_list_filtered, key=lambda k: (k['rank'], k['scripts'], k['position']))

                #sort final list - this is a round-robin script order 
                sorted_exms_list_robin = sorted(exms_list_filtered, key=lambda k: (k['scripts'], k['rank'], k['position']))
                print(sorted_exms_list_robin)
                
            #get "best" examiner for apportionment
            if sorted_exms_list_robin:
                chosen_exm = sorted_exms_list_robin[0]['creditor']
                print(str(script_id) + ' script id given to examiner ' + str(chosen_exm))
                print('')
                print('')
                
                if chosen_exm is not None:
                    
                    #per_sid = UniqueCreditor.objects.get(exm_creditor_no=chosen_exm).per_sid
                    sessions = str(EarServerSettings.objects.get(pk=1).session_id_list).split(',')
                    this_exm = EnquiryPersonnelDetails.objects.filter(exm_creditor_no=chosen_exm,ass_code=script_obj.eps_ass_code,com_id=script_obj.eps_com_id,session__in=sessions).first().enpe_sid
                    ScriptApportionment.objects.create(
                        enpe_sid = this_exm,
                        ec_sid =  script_obj
                        #script_marked is default to 0
                    )
                    if EnquiryComponents.objects.get(ec_sid=script_id).erp_sid.service_code == '3':
                        if not TaskManager.objects.filter(ec_sid=script_id, task_id='S3SEND',task_completion_date = None).exists():
                            TaskManager.objects.create(
                                enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task_enquiry_id),
                                ec_sid = EnquiryComponents.objects.get(ec_sid=script_id),
                                task_id = TaskTypes.objects.get(task_id = 'S3SEND'),
                                task_assigned_to = None,
                                task_assigned_date = None,
                                task_completion_date = None
                            )	
                    else:
                        if EnquiryComponents.objects.get(ec_sid=script_id).script_type == "RM Assessor":
                            TaskManager.objects.create(
                                enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task_enquiry_id),
                                ec_sid = EnquiryComponents.objects.get(ec_sid=script_id),
                                task_id = TaskTypes.objects.get(task_id = 'BOTAPP'),
                                task_assigned_to = User.objects.get(username='RPABOT'),
                                task_assigned_date = timezone.now(),
                                task_completion_date = None
                            )
                            TaskManager.objects.create(
                                enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task_enquiry_id),
                                ec_sid = EnquiryComponents.objects.get(ec_sid=script_id),
                                task_id = TaskTypes.objects.get(task_id = 'NEWMIS'),
                                task_assigned_to = User.objects.get(username='NovaServer'),
                                task_assigned_date = timezone.now(),
                                task_completion_date = None
                            )
                            TaskManager.objects.create(
                                enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task_enquiry_id),
                                ec_sid = EnquiryComponents.objects.get(ec_sid=script_id),
                                task_id = TaskTypes.objects.get(task_id = 'ESMCSV'),
                                task_assigned_to = None,
                                task_assigned_date = None,
                                task_completion_date = None
                            )
                        else:
                            TaskManager.objects.create(
                                enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task_enquiry_id),
                                ec_sid = EnquiryComponents.objects.get(ec_sid=script_id),
                                task_id = TaskTypes.objects.get(task_id = 'NRMACC'),
                                task_assigned_to = None,
                                task_assigned_date = None,
                                task_completion_date = None
                            )		
                else:
                    #AUTAPP not successful, send to manual apportionement
                    TaskManager.objects.create(
                        enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task_enquiry_id),
                        ec_sid = EnquiryComponents.objects.get(ec_sid=script_id),
                        task_id = TaskTypes.objects.get(task_id = 'MANAPP'),
                        task_assigned_to = None,
                        task_assigned_date = None,
                        task_completion_date = None
                    )            
            else:
                #AUTAPP not successful, send to manual apportionement - because no examiners in panel
                TaskManager.objects.create(
                    enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task_enquiry_id),
                    ec_sid = EnquiryComponents.objects.get(ec_sid=script_id),
                    task_id = TaskTypes.objects.get(task_id = 'MANAPP'),
                    task_assigned_to = None,
                    task_assigned_date = None,
                    task_completion_date = None
                )     





        #complete the task
        TaskManager.objects.filter(pk=task_pk,task_id='AUTAPP').update(task_completion_date=timezone.now())  

    end_time = datetime.datetime.now()
    print(end_time - start_time)      

run_algo()