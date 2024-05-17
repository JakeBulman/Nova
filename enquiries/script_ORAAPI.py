import django
import os 
import cx_Oracle
from django.utils import timezone

django.setup() 

##pull data from the final staging table and save it to a df
from enquiries.models import DjangoStagingTableAPP, DjangoStagingTableMAR, TaskManager, CentreEnquiryRequests, EnquiryComponents, TaskTypes, RpaFailureAudit
APIAPP_data = DjangoStagingTableAPP.objects.filter(copied_to_est=0) ##updateflag is the column that identifies if rows have been moved
APIMAR_data = DjangoStagingTableMAR.objects.filter(copied_to_est=0) ##updateflag is the column that identifies if rows have been moved
##APIMAR_data = DjangoStagingTableMAR.objects.filter()

##oracle creds

oracle_dsn = cx_Oracle.makedsn() ##oracle_host, oracle_port, service_name
oracle_conn = cx_Oracle.connect() ##oracle_user, oracle_password, dsn=oracle_dsn

cursor = oracle_conn.cursor() 

for item in APIAPP_data:
    try:
        cursor.execute("""
            INSERT INTO :oracleDB (enpe_sid, ec_sid, eb_sid, per_sid, pan_sid) VALUES (:enpe_sid, :ec_sid, :eb_sid, :per_sid, :pan_sid)
    """,{
        'oracleDB': 'dbname',
        'enpe_sid': item.enpe_sid,
        'ec_sid': item.ec_sid,
        'eb_sid': item.eb_sid,
        'per_sid': item.per_sid,
        'pan_sid': item.pan_sid,
    })
        DjangoStagingTableAPP.objects.filter(pk=item.pk).update(copied_to_est=1)
        oracle_conn.commit()
        print("Data Transfer has been completed")
    except Exception as e:
        script_id = item.ec_sid
        DjangoStagingTableAPP.objects.filter(pk=item.pk).update(error_status= f"{e}")
        if not TaskManager.objects.filter(ec_sid=EnquiryComponents.objects.only('ec_sid').get(ec_sid=script_id), task_id='BOTAPF',task_completion_date = None).exists():
                this_task = TaskManager.objects.create(
                    enquiry_id = CentreEnquiryRequests.objects.get(enquiries__enquiry_parts__ec_sid=script_id),
                    ec_sid = EnquiryComponents.objects.get(ec_sid=script_id),
                    task_id = TaskTypes.objects.get(task_id = 'BOTAPF'),
                    task_assigned_to = None,
                    task_assigned_date = None,
                    task_completion_date = None
                )
                this_task.refresh_from_db()
                print(this_task.pk)
                RpaFailureAudit.objects.create(
                    rpa_task_key = TaskManager.objects.get(pk=this_task.pk),
                    failure_reason = f"{e}"
                )
        #complete the task
    TaskManager.objects.filter(ec_sid=script_id,task_id='APIAPP').update(task_completion_date=timezone.now())


for item in APIMAR_data:
    try:
        cursor.execute("""
            INSERT INTO :oracleDB (ec_sid, eb_sid, outcome_status, final_mark, justification_code) VALUES (:ec_sid, :eb_sid, :outcome_status, :final_mark, :justification_code)
    """,{
         'oracleDB': 'dbname',
         'ec_sid': item.ec_sid,
         'eb_sid': item.eb_sid,
         'outcome_status': item.outcome_status,
         'final_mark': item.final_mark,
         'justification_code': item.justification_code,
    })
        DjangoStagingTableMAR.objects.filter(pk=item.pk).update(copied_to_est=1)
        oracle_conn.commit()
        print("Data Transfer has been completed")
    except Exception as e:
        script_id = item.ec_sid
        DjangoStagingTableMAR.objects.filter(pk=item.pk).update(error_status= f"{e}")
        if not TaskManager.objects.filter(ec_sid=EnquiryComponents.objects.only('ec_sid').get(ec_sid=script_id), task_id='BOTMAF',task_completion_date = None).exists():
                this_task = TaskManager.objects.create(
                    enquiry_id = CentreEnquiryRequests.objects.get(enquiries__enquiry_parts__ec_sid=script_id),
                    ec_sid = EnquiryComponents.objects.get(ec_sid=script_id),
                    task_id = TaskTypes.objects.get(task_id = 'BOTMAF'),
                    task_assigned_to = None,
                    task_assigned_date = None,
                    task_completion_date = None
                )
                this_task.refresh_from_db()
                print(this_task.pk)
                RpaFailureAudit.objects.create(
                    rpa_task_key = TaskManager.objects.get(pk=this_task.pk),
                    failure_reason = f"{e}"
                )
        #complete the task
    TaskManager.objects.filter(ec_sid=script_id,task_id='APIMAR').update(task_completion_date=timezone.now())



##add a column in the ear_stagingtbl that flags if there's an error (value e) -- will update when exception is caught
##send an email summary per day -- those not updated and has no errorflag

