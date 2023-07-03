import sys
import os
import django
import datetime
sys.path.append('C:/Dev/redepplan')
os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings'
django.setup()
from enquiries.models import TaskManager, EnquiryComponents, EnquiryComponentsPreviousExaminers, EnquiryPersonnel, EnquiryPersonnelDetails, ScriptApportionment, CentreEnquiryRequests, ExaminerConflicts, ExaminerAvailability
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth.models import User

# Create your views here.
def run_algo():
    start_time = datetime.datetime.now()
    print("Start Time:" + str(datetime.datetime.now()))

    for app_task in TaskManager.objects.filter(task_id='AUTAPP', task_completion_date__isnull=True):
    #for app_task in TaskManager.objects.filter(task_id='AUTAPP', task_completion_date__isnull=True):
        task_pk = app_task.pk
        script_id = app_task.ec_sid.ec_sid
        task_enquiry_id = app_task.enquiry_id.enquiry_id
        script_obj = EnquiryComponents.objects.get(ec_sid=script_id)
        conflicts = ExaminerConflicts.objects.all()
        examiner_detail_obj = EnquiryPersonnelDetails.objects.filter(ass_code=script_obj.eps_ass_code,com_id=script_obj.eps_com_id).order_by('exm_creditor_no')
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
                    prev_exm = EnquiryComponentsPreviousExaminers.objects.get(exm_creditor_position = exm_creditor_position, ec_sid = script_id)
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
                unavailability = None
                current_date = timezone.now().date()
                try:
                    unavailability = ExaminerAvailability.objects.get(creditor__exm_creditor_no = exm_creditor_no, 
                    unavailable_2_flag = "N", unavailability_start_date__lte = current_date - datetime.timedelta(days=5), unavailability_end_date__gte = current_date)
                except:
                    pass
                if unavailability is not None:
                    exm['rank'] = 4 #mark as non-viable

                #check for script overloading
                scripts = 0
                scripts_qc = ScriptApportionment.objects.filter(enpe_sid__per_sid__exm_creditor_no = exm_creditor_no).all()
                scripts_dict = scripts_qc.aggregate(Sum('script_marked'))
                print(scripts_dict)
                if scripts_dict['script_marked__sum'] is not None:
                    scripts = scripts_dict['script_marked__sum']
                #print(scripts)

                if scripts > 19:
                    exm['rank'] = 4 #mark as non-viable
                exm['scripts'] = scripts

            #print(exms_list)
            exms_list_filtered = []
            exms_list_filtered[:] = [d for d in exms_list if d.get('rank') != 4]
            #sort final list - this is a rank order 
            sorted_exms_list_rank = sorted(exms_list_filtered, key=lambda k: (k['rank'], k['scripts'], k['position']))

            #sort final list - this is a round-robin script order 
            sorted_exms_list_robin = sorted(exms_list_filtered, key=lambda k: (k['scripts'], k['rank'], k['position']))
            
            #get "best" examiner for apportionment

            #print(sorted_exms_list_rank)
            #print(script_obj.ec_sid)
            #print(exms_list)
        if sorted_exms_list_robin:
            chosen_exm = sorted_exms_list_robin[0]['creditor']
            #print(chosen_exm)
            
            if chosen_exm is not None:
                
                #per_sid = UniqueCreditor.objects.get(exm_creditor_no=chosen_exm).per_sid
                this_exm = EnquiryPersonnelDetails.objects.get(exm_creditor_no=chosen_exm,ass_code=script_obj.eps_ass_code,com_id=script_obj.eps_com_id).enpe_sid
                ScriptApportionment.objects.create(
                    enpe_sid = this_exm,
                    ec_sid =  script_obj
                    #script_marked is default to 0
                )

                TaskManager.objects.create(
                    enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task_enquiry_id),
                    ec_sid = EnquiryComponents.objects.get(ec_sid=script_id),
                    task_id = 'BOTAPP',
                    task_assigned_to = User.objects.get(id=14),
                    task_assigned_date = timezone.now(),
                    task_completion_date = None
                )
                TaskManager.objects.create(
                    enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task_enquiry_id),
                    ec_sid = EnquiryComponents.objects.get(ec_sid=script_id),
                    task_id = 'NEWMIS',
                    task_assigned_to = None,
                    task_assigned_date = None,
                    task_completion_date = None
                )
                TaskManager.objects.create(
                    enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task_enquiry_id),
                    ec_sid = EnquiryComponents.objects.get(ec_sid=script_id),
                    task_id = 'ESMCSV',
                    task_assigned_to = None,
                    task_assigned_date = None,
                    task_completion_date = None
                )
            else:
                #AUTAPP not successful, send to manual apportionement
                TaskManager.objects.create(
                    enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task_enquiry_id),
                    ec_sid = EnquiryComponents.objects.get(ec_sid=script_id),
                    task_id = 'MANAPP',
                    task_assigned_to = None,
                    task_assigned_date = None,
                    task_completion_date = None
                )            
        else:
            #AUTAPP not successful, send to manual apportionement - because no examiners in panel
            TaskManager.objects.create(
                enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task_enquiry_id),
                ec_sid = EnquiryComponents.objects.get(ec_sid=script_id),
                task_id = 'MANAPP',
                task_assigned_to = None,
                task_assigned_date = None,
                task_completion_date = None
            )      
        #complete the task
        TaskManager.objects.filter(pk=task_pk,task_id='AUTAPP').update(task_completion_date=timezone.now())  

    end_time = datetime.datetime.now()
    print(end_time - start_time)      

run_algo()