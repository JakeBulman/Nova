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
    # for task in TaskManager.objects.filter(task_id='SCRREN', task_completion_date__isnull=True):
    for file in os.listdir("\\\\filestorage\cie\Operations\Results Team\Enquiries About Results\\0.ScriptServices\From ESM\\"):
        if file.endswith(".pdf"):
            print(file)
            centre = file.split('_')[0]
            syll = file.split('_')[2]
            comp = file.split('_')[3]
            cand = file.split('_')[4]

            print(' '.join([centre,syll,comp,cand]))
            script = None
            if EnquiryComponents.objects.filter(erp_sid__eps_centre_id=centre,eps_ass_code=syll,eps_com_id=comp,erp_sid__eps_cand_id=cand).exists():
                #fetch out ids based on cent/syll/comp/cand
                script = EnquiryComponents.objects.get(erp_sid__eps_centre_id=centre,eps_ass_code=syll,eps_com_id=comp,erp_sid__eps_cand_id=cand)
                if TaskManager.objects.filter(ec_sid=script.ec_sid,task_id='SCRREN', task_completion_date__isnull=True).exists():
                    task = TaskManager.objects.get(ec_sid=script.ec_sid,task_id='SCRREN')
                    enquiry_id = script.erp_sid.cer_sid.enquiry_id
                    #take backup copy of the file
                    shutil.copy(os.path.join("\\\\filestorage\cie\Operations\Results Team\Enquiries About Results\\0.ScriptServices\From ESM\\", file), os.path.join("\\\\filestorage\cie\Operations\Results Team\Enquiries About Results\\0.ScriptServices\From ESM\Completed\\", file))
                    #copy file to next location with new name
                    new_name = '_'.join([centre,'COS',enquiry_id,syll,comp,cand]) + '.pdf'
                    shutil.move(os.path.join("\\\\filestorage\cie\Operations\Results Team\Enquiries About Results\\0.ScriptServices\From ESM\\", file), os.path.join("\\\\filestorage\cie\Operations\Results Team\Enquiries About Results\\0.ScriptServices\To Check\\", new_name))
                if '1' in EnquiryComponents.objects.only('ec_sid').get(ec_sid=script.ec_sid).erp_sid.service_code:
                    if not TaskManager.objects.filter(ec_sid=script.ec_sid, task_id='CLERIC',task_completion_date = None).exists():
                        TaskManager.objects.create(
                            enquiry_id = CentreEnquiryRequests.objects.only('enquiry_id').get(enquiry_id=script.erp_sid.cer_sid.enquiry_id),
                            ec_sid = EnquiryComponents.objects.only('ec_sid').get(ec_sid=script.ec_sid),
                            task_id = TaskTypes.objects.get(task_id = 'CLERIC'),
                            task_assigned_to = None,
                            task_assigned_date = None,
                            task_completion_date = None
                        )
                else:
                    TaskManager.objects.create(
                        enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task.enquiry_id.enquiry_id),
                        ec_sid = EnquiryComponents.objects.get(ec_sid=task.ec_sid.ec_sid),
                        task_id = TaskTypes.objects.get(task_id = 'SCRCHE'),
                        task_assigned_to = None,
                        task_assigned_date = None,
                        task_completion_date = None
                    )
                #Complete task
                TaskManager.objects.filter(pk=task.pk,task_id='SCRREN').update(task_completion_date=timezone.now())   

run_algo()