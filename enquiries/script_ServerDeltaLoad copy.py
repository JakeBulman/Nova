import sys
import os
import django
import datetime
import pyodbc
import pandas as pd
from openpyxl import load_workbook
import re
from django.conf import settings
from django.utils.timezone import make_aware
from dateutil.parser import parse
from email.message import EmailMessage
import smtplib
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

from enquiries.models import CentreEnquiryRequests, EnquiryRequestParts, EnquiryComponents, EnquiryPersonnel, EnquiryPersonnelDetails, EnquiryBatches, EnquiryComponentElements, TaskManager, UniqueCreditor, EnquiryComponentsHistory, EnquiryComponentsExaminerChecks, TaskTypes, EarServerSettings, EnquiryGrades, EnquiryDeadline, ExaminerPanels, MarkTolerances, ScaledMarks, CentreEnquiryRequestsExtra, EnquiryRequestPartsExtra, EnquiryComponentsExtra

def load_core_tables():

    start_time = datetime.datetime.now()
    print("Start Time:" + str(datetime.datetime.now()))
    EarServerSettings.objects.update(delta_load_status='Delta Load Starting, first table loading')

    #Limits enquiries to session or enquiry list
    session_id = EarServerSettings.objects.first().session_id_list
    enquiry_id_list = EarServerSettings.objects.first().enquiry_id_list
    if enquiry_id_list != '':
        enquiry_id_list = ' and cer.sid in (' + enquiry_id_list + ')'

    print("ENQ:" + enquiry_id_list)

    # # # Get datalake data - Centre Enquiry Requests
    # with pyodbc.connect("DSN=Impala DL", autocommit=True) as conn:
    #     df = pd.read_sql(f'''
    #         select distinct
    #         cer.sid as enquiry_id,
    #         cer.status as enquiry_status,
    #         cer.created_datetime as eps_creation_date,
    #         cer.completed_datetime as eps_completion_date,
    #         cer.acknowledge_letter_ind as eps_ack_letter_ind,
    #         cer.ses_sid as eps_ses_sid,
    #         cer.cnu_id as centre_id,
    #         cer.created_by as created_by,
    #         cer.cie_direct_id as cie_direct_id
    #         from ar_meps_req_prd.centre_enquiry_requests cer
    #         left join ar_meps_req_prd.enquiry_request_parts erp
    #         on erp.cer_sid = cer.sid
    #         where ses_sid in ({session_id}) 
    #         and erp.es_service_code in ('1','1S','2','2P','2PS','2S','ASC','ASR','3')
    #         {enquiry_id_list}
    #                             ''', conn)
    #     print(df)
    
    # def insert_to_model_cer(row):
    #     if CentreEnquiryRequests.objects.filter(enquiry_id=row['enquiry_id']).exists():
    #         CentreEnquiryRequests.objects.filter(enquiry_id=row['enquiry_id']).update(
    #             enquiry_id = row['enquiry_id'],
    #             enquiry_status = row['enquiry_status'],
    #             eps_creation_date = make_aware(parse(str(row['eps_creation_date']))),
    #             eps_completion_date = make_aware(parse(str(row['eps_completion_date']))),
    #             eps_ack_letter_ind = row['eps_ack_letter_ind'],
    #             eps_ses_sid = str(row['eps_ses_sid'])[:5],
    #             centre_id = row['centre_id'][:5],
    #             created_by = row['created_by'][:50],
    #             cie_direct_id = str(row['cie_direct_id'])[:7], 
    #         )
    #     else:
    #         CentreEnquiryRequests.objects.create(
    #             enquiry_id = row['enquiry_id'],
    #             enquiry_status = row['enquiry_status'],
    #             eps_creation_date = make_aware(parse(str(row['eps_creation_date']))),
    #             eps_completion_date = make_aware(parse(str(row['eps_completion_date']))),
    #             eps_ack_letter_ind = row['eps_ack_letter_ind'],
    #             eps_ses_sid = str(row['eps_ses_sid'])[:5],
    #             centre_id = row['centre_id'][:5],
    #             created_by = row['created_by'][:50],
    #             cie_direct_id =  str(row['cie_direct_id'])[:7],
    #             ministry_flag = None
    #         )

    # df.apply(insert_to_model_cer, axis=1)
    # print("CER loaded:" + str(datetime.datetime.now()))
    # EarServerSettings.objects.update(delta_load_status='Table 1 of 15 loaded, Centre Enquiry Requests')

    # for enquiry in CentreEnquiryRequests.objects.all():
    #     centre_id = enquiry.centre_id
    #     if re.search("^S[0-9]",centre_id):
    #         enquiry.ministry_flag = 'S'
    #         enquiry.save()
    #     if re.search("^MU",centre_id):
    #         enquiry.ministry_flag = 'MU'
    #         enquiry.save()

    # for enquiry in CentreEnquiryRequests.objects.all():
    #     enquiry_id = enquiry.enquiry_id
    #     if not TaskManager.objects.filter(enquiry_id=enquiry_id,task_id_id = 'INITCH').exists():
    #         TaskManager.objects.create(
    #             enquiry_id = CentreEnquiryRequests.objects.only('enquiry_id').get(enquiry_id=enquiry_id),
    #             ec_sid = None,
    #             task_id = TaskTypes.objects.get(task_id = 'INITCH'),
    #             task_assigned_to = None,
    #             task_assigned_date = None,
    #             task_completion_date = None
    #         )

    to_insert = []
    #for enquiry in CentreEnquiryRequests.objects.all():
    for enquiry in CentreEnquiryRequests.objects.filter(enquiry_id='1429890.0'):
        enquiry_id = enquiry.enquiry_id
        enquiry_obj = enquiry
        to_insert.append(
            TaskManager(
                enquiry_id = enquiry_obj,
                ec_sid = None,
                task_id = TaskTypes.objects.get(task_id = 'INITCH'),
                task_assigned_to = None,
                task_assigned_date = None,
                task_completion_date = None
            )
        )
        print(enquiry_id)
    print('Bulk insert start')
    TaskManager.objects.bulk_create(to_insert,update_conflicts=True,unique_fields=['enquiry_id'],update_fields=['ec_sid','task_id'])
    print('Bulk insert end')


            # TaskManager(
            #     enquiry_id = CentreEnquiryRequests.objects.only('enquiry_id').get(enquiry_id=enquiry_id),
            #     ec_sid = None,
            #     task_id = TaskTypes.objects.get(task_id = 'INITCH'),
            #     task_assigned_to = None,
            #     task_assigned_date = None,
            #     task_completion_date = None
            # )

    print("IEC loaded:" + str(datetime.datetime.now()))


load_core_tables()
