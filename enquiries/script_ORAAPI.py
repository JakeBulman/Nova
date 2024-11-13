import django
import sys
import os 
import cx_Oracle
from django.utils import timezone

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

##pull data from the final staging table and save it to a df
from enquiries.models import DjangoStagingTableAPP, DjangoStagingTableMAR, TaskManager, CentreEnquiryRequests, EnquiryComponents, TaskTypes, RpaFailureAudit
APIAPP_data = DjangoStagingTableAPP.objects.filter(copied_to_est=0) ##copied_to_est is the column that identifies if rows have been moved
APIMAR_data = DjangoStagingTableMAR.objects.filter(copied_to_est=0) ##copied_to_est is the column that identifies if rows have been moved

##oracle creds
#oracle_conn = cx_Oracle.connect('apitest123/testpassword@sddevap180:1521/novaoratest', mode = cx_Oracle.SYSDBA)
oracle_conn = cx_Oracle.connect('NOVARW/n0vaeps@udepsor010:1583/MDEV')

cursor = oracle_conn.cursor() 

for item in APIAPP_data:
    DjangoStagingTableAPP.objects.filter(pk=item.pk).update(error_status= '')
    try :
        cursor.execute("""
            INSERT INTO ETL_PRD.EAR_CLERICAL_MARKS_STAGING (start_date,ses_sid,cer_sid,eb_sid,centre,ass_code,asv_ver_no,com_id,me_id,cand_no,old_mark) VALUES( :eps_creation_date, :eps_ses_sid, :enquiry_id, :eb_sid, :eps_centre_id, :eps_ass_code, :eps_ass_ver_no, :com_id, :me_id, :eps_cand_id, :ear_mark)
    """,{
        'eps_creation_date': item.eps_creation_date,
        'eps_ses_sid': item.eps_ses_sid,
        'enquiry_id' : item.enquiry_id.enquiry_id,
        'eb_sid': item.eb_sid.eb_sid,
        'eps_centre_id': item.eps_centre_id,
        'eps_ass_code': item.eps_ass_code,
        'eps_ass_ver_no': item.eps_ass_ver_no,
        'com_id': item.ec_sid.eps_com_id,
        'me_id': item.me_id,
        'eps_cand_id': item.eps_cand_id,
        'ear_mark': item.ear_mark
    })
        DjangoStagingTableAPP.objects.filter(pk=item.pk).update(copied_to_est=1)
        oracle_conn.commit()
        print("Data Transfer has been completed")
    except Exception as e:
        script_id = item.ec_sid.ec_sid
        DjangoStagingTableAPP.objects.filter(pk=item.pk).update(error_status= f"{e}")
        print(e)
        if not TaskManager.objects.filter(ec_sid=EnquiryComponents.objects.only('ec_sid').get(ec_sid=script_id), task_id='BOTAPF',task_completion_date = None).exists():
                this_task = TaskManager.objects.create(
                    enquiry_id = CentreEnquiryRequests.objects.get(enquiries__enquiry_parts__ec_sid=script_id),
                    ec_sid = EnquiryComponents.objects.get(ec_sid=script_id),
                    task_id = TaskTypes.objects.get(task_id = 'BOTAPF'),
                    task_assigned_to = None,
                    task_assigned_date = None,
                    task_completion_date = None
                )
                TaskManager.objects.filter(ec_sid=script_id, task_id='APIAPP').update(task_completion_date = timezone.now())
                this_task.refresh_from_db()
                print(this_task.pk)
                RpaFailureAudit.objects.create(
                    rpa_task_key = TaskManager.objects.get(pk=this_task.pk),
                    failure_reason = f"{e}"
                )

# for item in APIMAR_data:
#     try:
#         cursor.execute("""
#             INSERT INTO :oracleDB (ec_sid, eb_sid, outcome_status, final_mark, justification_code) VALUES (:ec_sid, :eb_sid, :outcome_status, :final_mark, :justification_code)
#     """,{
#          'oracleDB': 'APITEST123.APIMAR',
#          'ec_sid': item.ec_sid,
#          'eb_sid': item.eb_sid,
#          'outcome_status': item.outcome_status,
#          'final_mark': item.final_mark,
#          'justification_code': item.justification_code,
#     })
#         DjangoStagingTableMAR.objects.filter(pk=item.pk).update(copied_to_est=1)
#         oracle_conn.commit()
#         print("Data Transfer has been completed")
#     except Exception as e:
#         script_id = item.ec_sid
#         DjangoStagingTableMAR.objects.filter(pk=item.pk).update(error_status= f"{e}")
#         if not TaskManager.objects.filter(ec_sid=EnquiryComponents.objects.only('ec_sid').get(ec_sid=script_id), task_id='BOTMAF',task_completion_date = None).exists():
#                 this_task = TaskManager.objects.create(
#                     enquiry_id = CentreEnquiryRequests.objects.get(enquiries__enquiry_parts__ec_sid=script_id),
#                     ec_sid = EnquiryComponents.objects.get(ec_sid=script_id),
#                     task_id = TaskTypes.objects.get(task_id = 'BOTMAF'),
#                     task_assigned_to = None,
#                     task_assigned_date = None,
#                     task_completion_date = None
#                 )
#                 this_task.refresh_from_db()
#                 print(this_task.pk)
#                 RpaFailureAudit.objects.create(
#                     rpa_task_key = TaskManager.objects.get(pk=this_task.pk),
#                     failure_reason = f"{e}"
#                 )

# ##send an email summary per day -- those not updated and has no errorflag

