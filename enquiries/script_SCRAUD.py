import sys
import os
import django
from django.utils import timezone
import datetime
import shutil

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

from enquiries.models import TaskManager, EnquiryComponents, CentreEnquiryRequests, TaskTypes
from django.contrib.auth.models import User

def run_algo():
    for task in TaskManager.objects.filter(task_id='SCRAUD', task_completion_date__isnull=True):
        scr_complete_check = False
        enquiry_id = task.enquiry_id.enquiry_id
        #create list of all comps in enq
        comp_list_full = []
        for comp in EnquiryComponents.objects.filter(erp_sid__cer_sid=enquiry_id):
            comp_list_full.append(comp.ec_sid)
        comp_list_scraud = []
        #does script exist for all comps in enq
        for file in os.listdir("\\\\filestorage\cie\Operations\Results Team\Enquiries About Results\\0.ScriptServices\Ready To Upload\\"):
            if file.endswith(".pdf"):
                centre = file.split('_')[0]
                enquiry_id = file.split('_')[2]
                syll = file.split('_')[3]
                comp = file.split('_')[4]
                cand = file.split('_')[5].split('.')[0]
                script_id = None
                if EnquiryComponents.objects.filter(erp_sid__eps_centre_id=centre,erp_sid__cer_sid=enquiry_id,eps_ass_code=syll,eps_com_id=comp,erp_sid__eps_cand_id=cand).exists():
                    #fetch out ids based on cent/enq/syll/comp/cand
                    script_id = EnquiryComponents.objects.get(erp_sid__eps_centre_id=centre,erp_sid__cer_sid=enquiry_id,eps_ass_code=syll,eps_com_id=comp,erp_sid__eps_cand_id=cand).ec_sid
                    #check if all prior checks are complete
                    task_type = ['CLERIC','SCRCHE','SCRREQ']
                    if not TaskManager.objects.filter(task_id__in=task_type, ec_sid=script_id, task_completion_date__isnull=True).exists():   
                        if script_id not in comp_list_scraud:
                            comp_list_scraud.append(script_id)

        comp_list_full.sort()
        comp_list_scraud.sort()
        print(comp_list_full,comp_list_scraud)
        scr_complete_check = comp_list_full == comp_list_scraud
        
        if scr_complete_check:
            #Move files for this enquiry ID to final folder
            for file in os.listdir("\\\\filestorage\cie\Operations\Results Team\Enquiries About Results\\0.ScriptServices\Ready To Upload\\"):
                if file.endswith(".pdf"):
                    print(file)
                    centre = file.split('_')[0]
                    enquiry_id = file.split('_')[2]
                    syll = file.split('_')[3]
                    comp = file.split('_')[4]
                    cand = file.split('_')[5].split('.')[0]
                    print(' '.join([centre,enquiry_id,syll,comp,cand]))
                    if enquiry_id == task.enquiry_id.enquiry_id:
                        #take backup copy of the file
                        shutil.copy(os.path.join("\\\\filestorage\cie\Operations\Results Team\Enquiries About Results\\0.ScriptServices\Ready To Upload\\", file), os.path.join("\\\\filestorage\cie\Operations\Results Team\Enquiries About Results\\0.ScriptServices\Ready To Upload\Backup\\", file))
                        #copy file to next location with new name
                        new_name = '_'.join([centre,'COS',enquiry_id,syll,comp,cand]) + '.pdf'
                        shutil.move(os.path.join("\\\\filestorage\cie\Operations\Results Team\Enquiries About Results\\0.ScriptServices\Ready To Upload\\", file), os.path.join("\\\\filestorage\cie\Operations\Results Team\Enquiries About Results\\0.ScriptServices\Passed Script Audit\\", new_name))

            #Marks tasks complete and continue chain
            print(str(enquiry_id) + " passes SCRAUD")
            TaskManager.objects.create(
                enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
                ec_sid = None,
                task_id = TaskTypes.objects.get(task_id = 'LETSCR'),
                task_assigned_to = None,
                task_assigned_date = None,
                task_completion_date = None
            )
                
            TaskManager.objects.filter(pk=task.pk,task_id='SCRAUD').update(task_completion_date=timezone.now())   

run_algo()