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

    ec_list = [
        '2068992',
        '2069002',
        '2069138',
        '2069212',
        '2069246',
        '2069392',
        '2069426',
        '2069450',
        '2069674',
        '2069694',
        '2069826',
        '2069822',
        '2069850',
        '2069878',
        '2069898',
        '2069990',
        '2070184',
        '2070446',
        '2072044',
        '2072058',
        '2072384',
        '2072422',
        '2072442',
        '2072464',
        '2072660',
        '2072890',
        '2072884',
        '2072894',
        '2072914',
        '2072938',
        '2073016',
        '2073068',
        '2073200',
        '2073192',
        '2073172',
        '2073490',
        '2073620',
        '2074378',
        '2074796',
        '2074886',
        '2074970',
        '2075348',
        '2075440',
        '2075556',
        '2075836',
        '2075938',
        '2076222',
        '2076308',
        '2076588',
        '2076706',
        '2077450',
        '2077712',
        '2077724',
        '2077978',
        '2077990',
        '2078020',
        '2078012',
        '2078006',
        '2078038',
        '2078110',
        '2078112',
        '2078124',
        '2078178',
        '2078214',
        '2078370',
        '2078420',
        '2078458',
        '2078466',
        '2078462',
        '2078500',
        '2078496',
        '2078508',
        '2078514',
        '2078530',
        '2078776',
        '2078914',
        '2079028',
        '2079088',
        '2079092',
        '2079738',
        '2079984',
        '2081704',
        '2081782',
        '2081858',
        '2081862',
        '2082044',
        '2082236',
        '2082346',
        '2082378',
        '2082464',
        '2082622',
        '2082706',
        '2082754',
        '2082780',
        '2082816',
        '2082868',
        '2082884',
        '2082886',
        '2082998',
        '2083136',
        '2083588',
        '2083622',
        '2083744',
        '2084840',
        '2084858',
        '2084920',
        '2085416',
        '2085428',
        '2085534',
        '2085798',
        '2085904',
        '2085952',
        '2085990',
        '2086050',
        '2086062',
        '2086136',
        '2086780',
        '2086832',
        '2086920',
        '2087002',
        '2087156',
        '2087266',
        '2087256',
        '2087272',
        '2087348',
        '2087396',
        '2087398',
        '2087458',
        '2087474',
        '2087516',
        '2087534',
        '2087546',
        '2087738',
        '2087734',
        '2087742',
        '2087870',
        '2087930',
        '2088008',
        '2088032',
        '2088082',
        '2088140',
        '2088148',
        '2088154',
        '2088246',
        '2088836',
        '2089148',
        '2089170',

    ]
    script_list = []
    for app_task in TaskManager.objects.filter(task_id='AUTAPP', ec_sid_id__in = ec_list):
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
            # TaskManager.objects.create(
            #     enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task_enquiry_id),
            #     ec_sid = EnquiryComponents.objects.get(ec_sid=script_id),
            #     task_id = TaskTypes.objects.get(task_id = 'MANAPP'),
            #     task_assigned_to = None,
            #     task_assigned_date = None,
            #     task_completion_date = None
            # )      
            print('MANAPP')
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
            #print("exms_list:")
            #print(exms_list)
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
                    current_date = timezone.now().date() - datetime.timedelta(days=5)
                    print(current_date)
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

                #print(exms_list)
                exms_list_filtered = []
                exms_list_filtered[:] = [d for d in exms_list if d.get('rank') != 4]
                #sort final list - this is a rank order 
                sorted_exms_list_rank = sorted(exms_list_filtered, key=lambda k: (k['rank'], k['scripts'], k['position']))

                #sort final list - this is a round-robin script order 
                sorted_exms_list_robin = sorted(exms_list_filtered, key=lambda k: (k['scripts'], k['rank'], k['position']))
                #print(sorted_exms_list_robin)
                
            #get "best" examiner for apportionment
            if sorted_exms_list_robin:
                chosen_exm = sorted_exms_list_robin[0]['creditor']
                script_list.append([script_id,chosen_exm,sorted_exms_list_robin[0]['position']])
                print(str(script_id) + ' script id given to examiner ' + str(chosen_exm))
    for a in script_list:
        print(a)
            #     if chosen_exm is not None:
                    
            #         #per_sid = UniqueCreditor.objects.get(exm_creditor_no=chosen_exm).per_sid
            #         sessions = str(EarServerSettings.objects.get(pk=1).session_id_list).split(',')
            #         this_exm = EnquiryPersonnelDetails.objects.filter(exm_creditor_no=chosen_exm,ass_code=script_obj.eps_ass_code,com_id=script_obj.eps_com_id,session__in=sessions).first().enpe_sid
            #         ScriptApportionment.objects.create(
            #             enpe_sid = this_exm,
            #             ec_sid =  script_obj
            #             #script_marked is default to 0
            #         )
            #         if EnquiryComponents.objects.get(ec_sid=script_id).erp_sid.service_code == '3':
            #             if not TaskManager.objects.filter(ec_sid=script_id, task_id='S3SEND',task_completion_date = None).exists():
            #                 TaskManager.objects.create(
            #                     enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task_enquiry_id),
            #                     ec_sid = EnquiryComponents.objects.get(ec_sid=script_id),
            #                     task_id = TaskTypes.objects.get(task_id = 'S3SEND'),
            #                     task_assigned_to = None,
            #                     task_assigned_date = None,
            #                     task_completion_date = None
            #                 )	
            #         else:
            #             if EnquiryComponents.objects.get(ec_sid=script_id).script_type == "RM Assessor":
            #                 TaskManager.objects.create(
            #                     enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task_enquiry_id),
            #                     ec_sid = EnquiryComponents.objects.get(ec_sid=script_id),
            #                     task_id = TaskTypes.objects.get(task_id = 'BOTAPP'),
            #                     task_assigned_to = User.objects.get(username='RPABOT'),
            #                     task_assigned_date = timezone.now(),
            #                     task_completion_date = None
            #                 )
            #                 TaskManager.objects.create(
            #                     enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task_enquiry_id),
            #                     ec_sid = EnquiryComponents.objects.get(ec_sid=script_id),
            #                     task_id = TaskTypes.objects.get(task_id = 'NEWMIS'),
            #                     task_assigned_to = User.objects.get(username='NovaServer'),
            #                     task_assigned_date = timezone.now(),
            #                     task_completion_date = None
            #                 )
            #                 TaskManager.objects.create(
            #                     enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task_enquiry_id),
            #                     ec_sid = EnquiryComponents.objects.get(ec_sid=script_id),
            #                     task_id = TaskTypes.objects.get(task_id = 'ESMCSV'),
            #                     task_assigned_to = None,
            #                     task_assigned_date = None,
            #                     task_completion_date = None
            #                 )
            #             else:
            #                 TaskManager.objects.create(
            #                     enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task_enquiry_id),
            #                     ec_sid = EnquiryComponents.objects.get(ec_sid=script_id),
            #                     task_id = TaskTypes.objects.get(task_id = 'NRMACC'),
            #                     task_assigned_to = None,
            #                     task_assigned_date = None,
            #                     task_completion_date = None
            #                 )		
            #     else:
            #         #AUTAPP not successful, send to manual apportionement
            #         TaskManager.objects.create(
            #             enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task_enquiry_id),
            #             ec_sid = EnquiryComponents.objects.get(ec_sid=script_id),
            #             task_id = TaskTypes.objects.get(task_id = 'MANAPP'),
            #             task_assigned_to = None,
            #             task_assigned_date = None,
            #             task_completion_date = None
            #         )            
            # else:
            #     #AUTAPP not successful, send to manual apportionement - because no examiners in panel
            #     TaskManager.objects.create(
            #         enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task_enquiry_id),
            #         ec_sid = EnquiryComponents.objects.get(ec_sid=script_id),
            #         task_id = TaskTypes.objects.get(task_id = 'MANAPP'),
            #         task_assigned_to = None,
            #         task_assigned_date = None,
            #         task_completion_date = None
            #     )     





        # #complete the task
        # TaskManager.objects.filter(pk=task_pk,task_id='AUTAPP').update(task_completion_date=timezone.now())  

    end_time = datetime.datetime.now()
    print(end_time - start_time)      

run_algo()