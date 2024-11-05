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

from enquiries.models import TaskManager, ScriptApportionment,EnquiryComponentElements, DjangoStagingTableMAR, ScaledMarks, MisReturnData
from django.contrib.auth.models import User

def run_algo():
    for task in TaskManager.objects.filter(task_id='APIMAR', task_completion_date__isnull=True):
        ec_sid = task.ec_sid
        eb_sid = EnquiryComponentElements.objects.filter(ec_sid=task.ec_sid).first().eb_sid,
        eps_centre_id = ec_sid.erp_sid.eps_centre_id
        eps_cand_id = ec_sid.erp_sid.eps_cand_id

        scaled_mark = ScaledMarks.objects.filter(eps_ass_code=ec_sid.eps_ass_code,eps_com_id=ec_sid.eps_com_id,eps_cnu_id=ec_sid.erp_sid.eps_centre_id,eps_cand_no=ec_sid.erp_sid.eps_cand_id,eps_ses_sid=ec_sid.eps_ses_sid).first().scaled_mark
        keyed_mark_status = MisReturnData.objects.filter(ec_sid=ec_sid).first().keyed_mark_status
        if keyed_mark_status == 'Confirmed':
            mark_confirmed_ind = 'Y'
        elif keyed_mark_status == 'Changed':
            mark_confirmed_ind = 'N'
        else:
            mark_confirmed_ind = None
        final_mark = MisReturnData.objects.filter(ec_sid=ec_sid).first().final_mark
        selected_justification_code = MisReturnData.objects.filter(ec_sid=ec_sid).first().selected_justification_code



        if DjangoStagingTableMAR.objects.filter(ec_sid=ec_sid,copied_to_est=0).exists():
            DjangoStagingTableMAR.objects.filter(ec_sid=ec_sid,copied_to_est=0).update(
                ec_sid = ec_sid,
                eb_sid = eb_sid,
                eps_centre_id = eps_centre_id,
                eps_cand_id = eps_cand_id,
                scaled_mark = scaled_mark,
                mark_confirmed_ind = mark_confirmed_ind,
                final_mark = final_mark,
                selected_justification_code = selected_justification_code
            )
        else:
            DjangoStagingTableMAR.objects.create(
                ec_sid = ec_sid,
                eb_sid = eb_sid,
                eps_centre_id = eps_centre_id,
                eps_cand_id = eps_cand_id,
                scaled_mark = scaled_mark,
                mark_confirmed_ind = mark_confirmed_ind,
                final_mark = final_mark,
                selected_justification_code = selected_justification_code
            )


        #TaskManager.objects.filter(pk=task.pk,task_id='APIAPP').update(task_completion_date=timezone.now())   

run_algo()