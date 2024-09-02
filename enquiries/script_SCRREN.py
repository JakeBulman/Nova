import sys
import os
import django
from django.utils import timezone
import datetime
import shutil
import traceback

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

from enquiries.models import TaskManager, EnquiryComponents, CentreEnquiryRequests, TaskTypes, EarServerSettings
from django.contrib.auth.models import User

def run_algo():
    # for task in TaskManager.objects.filter(task_id='SCRREN', task_completion_date__isnull=True):
    for file in os.listdir("\\\\filestorage\cie\Operations\Results Team\Enquiries About Results\\0.ScriptServices\From ESM\\"):
        try:
            if file.endswith(".pdf"):
                print(file)
                centre = file.split('_')[0].strip()
                syll = file.split('_')[2].strip()
                comp = file.split('_')[3].strip()
                cand = file.split('_')[4].strip()
                sessions = str(EarServerSettings.objects.get(pk=1).session_id_list).split(',')
                print(sessions)

                print(' '.join([centre,syll,comp,cand]))
                script = None
                if EnquiryComponents.objects.filter(erp_sid__eps_centre_id=centre,eps_ass_code=syll,eps_com_id=comp,erp_sid__eps_cand_id=cand,eps_ses_sid__in=sessions).exists():
                    #fetch out ids based on cent/syll/comp/cand
                    scripts = EnquiryComponents.objects.filter(erp_sid__eps_centre_id=centre,eps_ass_code=syll,eps_com_id=comp,erp_sid__eps_cand_id=cand,eps_ses_sid__in=sessions)
                    for script in scripts:
                        if not TaskManager.objects.filter(ec_sid=script.ec_sid,task_id='SETBIE').exists():
                            print("Script:" + script.ec_sid + "// Enq:" + script.erp_sid.cer_sid.enquiry_id)
                            if TaskManager.objects.filter(ec_sid=script.ec_sid,task_id='SCRREN', task_completion_date__isnull=True).exists():
                                task = TaskManager.objects.get(ec_sid=script.ec_sid,task_id='SCRREN')
                                enquiry_id = script.erp_sid.cer_sid.enquiry_id
                                #take backup copy of the file
                                shutil.copy(os.path.join("\\\\filestorage\cie\Operations\Results Team\Enquiries About Results\\0.ScriptServices\From ESM\\", file), os.path.join("\\\\filestorage\cie\Operations\Results Team\Enquiries About Results\\0.ScriptServices\From ESM\Completed\\", file))
                                #copy file to next location with new name
                                new_name = '_'.join([centre,'COS',enquiry_id,syll,comp,cand]) + '.pdf'
                                if script.erp_sid.service_code == '2S':
                                    shutil.move(os.path.join("\\\\filestorage\cie\Operations\Results Team\Enquiries About Results\\0.ScriptServices\From ESM\\", file), os.path.join("\\\\filestorage\cie\Operations\Results Team\Enquiries About Results\\0.ScriptServices\To Check - 2S\\", new_name))
                                else:
                                    shutil.move(os.path.join("\\\\filestorage\cie\Operations\Results Team\Enquiries About Results\\0.ScriptServices\From ESM\\", file), os.path.join("\\\\filestorage\cie\Operations\Results Team\Enquiries About Results\\0.ScriptServices\To Check\\", new_name))
                                service_code = EnquiryComponents.objects.only('ec_sid').get(ec_sid=script.ec_sid).erp_sid.service_code
                                if service_code == 'ASC' or service_code == 'ASR' or '1' in service_code:
                                    if not TaskManager.objects.filter(ec_sid=script.ec_sid, task_id='CLERIC',task_completion_date = None).exists():
                                        TaskManager.objects.create(
                                            enquiry_id = CentreEnquiryRequests.objects.only('enquiry_id').get(enquiry_id=script.erp_sid.cer_sid.enquiry_id),
                                            ec_sid = EnquiryComponents.objects.only('ec_sid').get(ec_sid=script.ec_sid),
                                            task_id = TaskTypes.objects.get(task_id = 'CLERIC'),
                                            task_assigned_to = None,
                                            task_assigned_date = None,
                                            task_completion_date = None
                                        )
                                        TaskManager.objects.filter(pk=task.pk,task_id='SCRREN').update(task_completion_date=timezone.now())
                                else:
                                    if not TaskManager.objects.filter(ec_sid=script.ec_sid, task_id='SCRCHE',task_completion_date = None).exists():
                                        TaskManager.objects.create(
                                            enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=script.erp_sid.cer_sid.enquiry_id),
                                            ec_sid = EnquiryComponents.objects.get(ec_sid=script.ec_sid),
                                            task_id = TaskTypes.objects.get(task_id = 'SCRCHE'),
                                            task_assigned_to = None,
                                            task_assigned_date = None,
                                            task_completion_date = None
                                        )
                                        TaskManager.objects.filter(pk=task.pk,task_id='SCRREN').update(task_completion_date=timezone.now())
                                
                            else:
                                print("No available SCRREN task")
                else:
                    print("Component not found in EC") 
        except:
            print(traceback.format_exc()) 

run_algo()