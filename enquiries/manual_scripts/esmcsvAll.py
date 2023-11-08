
import sys
import os
import django
from django.utils import timezone
from django.conf import settings
import csv, os

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

from enquiries.models import ScriptApportionment, EnquiryPersonnelDetails, EsmcsvDownloads, EnquiryComponentElements, TaskManager

ec_queryset = TaskManager.objects.filter(task_id='ESMCSV', ec_sid__script_id__eb_sid__eb_sid__isnull=False)
if ec_queryset.count() > 0:
    file_timestamp = timezone.now().strftime("%m_%d_%Y_%H_%M_%S") + ".csv"
    file_location = os.path.join(settings.MEDIA_ROOT, "downloads", file_timestamp).replace('\\', '/')
    print(file_location)	
    with open(file_location, 'w', newline='') as file:
        file.truncate()
        writer = csv.writer(file)
        for s in ec_queryset:
            if ScriptApportionment.objects.filter(ec_sid = s.ec_sid, apportionment_invalidated = 0).exists():
                syllcomp = s.ec_sid.eps_ass_code + "/" + s.ec_sid.eps_com_id
                batch = EnquiryComponentElements.objects.get(ec_sid = s.ec_sid).eb_sid.eb_sid
                session = s.ec_sid.eps_ses_name
                candidate = s.ec_sid.erp_sid.eps_cand_id
                centre = s.ec_sid.erp_sid.eps_centre_id
                examiner_name = ScriptApportionment.objects.get(ec_sid = s.ec_sid, apportionment_invalidated = 0).enpe_sid.per_sid.exm_forename + " " + ScriptApportionment.objects.get(ec_sid = s.ec_sid, apportionment_invalidated = 0).enpe_sid.per_sid.exm_surname
                examiner_pos = EnquiryPersonnelDetails.objects.filter(enpe_sid = ScriptApportionment.objects.get(ec_sid = s.ec_sid, apportionment_invalidated = 0).enpe_sid).first().exm_examiner_no
                creditor_number = ScriptApportionment.objects.get(ec_sid = s.ec_sid, apportionment_invalidated = 0).enpe_sid.per_sid.exm_creditor_no

                writer.writerow([syllcomp,batch,session,candidate,centre,examiner_name, examiner_pos, creditor_number, ""])

    EsmcsvDownloads.objects.create(
        document = file_location,
        file_name = file_timestamp,
        download_count = 0,
        archive_count = 0
        )
    
        #Get username to filter tasks

    