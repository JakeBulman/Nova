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
    print('UAT - Check')
    path = os.path.join('C:\\Dev\\nova')
    sys.path.append(path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings'

django.setup()

from enquiries.models import TaskManager, ScriptApportionment,EnquiryComponentElements, DjangoStagingTableAPP, EnquiryComponents, EnquiryComponentsHistory
from django.contrib.auth.models import User

def run_algo():
    for task in TaskManager.objects.filter(task_id='APIAPP', task_completion_date__isnull=True):

        script_apportion_details = ScriptApportionment.objects.get(ec_sid=task.ec_sid.ec_sid,apportionment_invalidated=0)

        #table Apportionment Clerical Check
        ec_sid = EnquiryComponents.objects.filter(ec_sid=task.ec_sid).first()
        eb_sid = EnquiryComponentElements.objects.filter(ec_sid=task.ec_sid).first().eb_sid
        eps_creation_date = ec_sid.erp_sid.cer_sid.eps_creation_date
        eps_ses_sid = ec_sid.erp_sid.cer_sid.eps_ses_sid
        enquiry_id = ec_sid.erp_sid.cer_sid.enquiry_id
        
        eps_centre_id = ec_sid.erp_sid.eps_centre_id
        eps_ass_code = ec_sid.erp_sid.eps_ass_code
        eps_ass_ver_no = ec_sid.erp_sid.eps_ass_ver_no
        com_id =  ec_sid.eps_com_id
        me_id = EnquiryComponentElements.objects.filter(ec_sid=task.ec_sid).first().me_id
        eps_cand_id = ec_sid.erp_sid.eps_cand_id
        ear_mark = EnquiryComponentsHistory.objects.filter(ec_sid=task.ec_sid)

        #table 2 Apportionment Examiner Selection
        enpe_sid = script_apportion_details.enpe_sid
        eb_sid = EnquiryComponentElements.objects.filter(ec_sid=task.ec_sid).first().eb_sid


        if DjangoStagingTableAPP.objects.filter(ec_sid=ec_sid,copied_to_est=0).exists():
            DjangoStagingTableAPP.objects.filter(ec_sid=ec_sid,copied_to_est=0).update(
                enpe_sid = enpe_sid,
                ec_sid = ec_sid,
                eb_sid = eb_sid,
                eps_creation_date = eps_creation_date,
                eps_ses_sid = eps_ses_sid,
                enquiry_id = enquiry_id,
                eps_centre_id = eps_centre_id,
                eps_ass_code = eps_ass_code,
                eps_ass_ver_no = eps_ass_ver_no,
                com_id = com_id,
                me_id = me_id,
                eps_cand_id = eps_cand_id,
                ear_mark = ear_mark
            )
        else:
            DjangoStagingTableAPP.objects.create(
                enpe_sid = enpe_sid,
                ec_sid = ec_sid,
                eb_sid = eb_sid,
                eps_creation_date = eps_creation_date,
                eps_ses_sid = eps_ses_sid,
                enquiry_id = enquiry_id,
                eps_centre_id = eps_centre_id,
                eps_ass_code = eps_ass_code,
                eps_ass_ver_no = eps_ass_ver_no,
                com_id = com_id,
                me_id = me_id,
                eps_cand_id = eps_cand_id,
                ear_mark = ear_mark
            )


        #TaskManager.objects.filter(pk=task.pk,task_id='APIAPP').update(task_completion_date=timezone.now())   

run_algo()