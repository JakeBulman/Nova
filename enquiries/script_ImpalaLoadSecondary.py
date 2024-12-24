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

import warnings
warnings.filterwarnings("ignore")

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



    # Get datalake data - Panels
    with pyodbc.connect("DSN=Impala DL", autocommit=True) as conn:
        df = pd.read_sql(f'''
                select distinct
                csce.ass_code as ass_code,
                csce.com_id as com_id,
                sp.name as sp_name,
                sp.ses_sid as sp_ses_sid,
                sdc.panel_size as panel_size
                from ar_meps_req_prd.enquiry_personnel enpe
                left join ar_meps_pan_prd.vw_delta_session_panel_positions spp
                on enpe.eper_per_sid = spp.per_sid and enpe.pan_sid = spp.stm_pan_sid
                left join  ar_meps_pan_prd.vw_delta_session_panels sp
                on sp.sid = spp.stm_pan_sid
                left join (select stm_pan_sid, count(*) as panel_size from ar_meps_pan_prd.vw_delta_session_panel_positions spp where spp.creditor_no is not null
                group by stm_pan_sid) sdc
                on sdc.stm_pan_sid = spp.stm_pan_sid
                left join ar_meps_ord_prd.centre_sess_comp_entries csce
                on sp.sid = csce.pan_sid
                where csce.ass_code is not null and
                sp.ses_sid in({session_id}) 
                                ''', conn)

    rolling_insert = []
    def insert_to_model(row):
        rolling_insert.append(
            ExaminerPanels(
                ses_ass_com = str(int(row['sp_ses_sid'])) + str(row['ass_code']) + str(row['com_id']),
                ses_sid = int(row['sp_ses_sid']),
                ass_code = row['ass_code'],
                com_id = row['com_id'],
                panel_name = row['sp_name'],
                panel_size = row['panel_size'],
                panel_notes = None
            )
        )

    df.apply(insert_to_model, axis=1)
    ExaminerPanels.objects.bulk_create(rolling_insert,update_conflicts=True,unique_fields=['ses_ass_com'],
                                              update_fields=['ses_sid','ass_code','com_id','panel_name','panel_size']
                                              )
    
    print("ECM_PAN loaded:" + str(datetime.datetime.now()))
    EarServerSettings.objects.update(delta_load_status='Table 7 of 15 loaded, Examiner Panels')






    # Get datalake data - Unique Creditors
    with pyodbc.connect("DSN=Impala DL", autocommit=True) as conn:
        df = pd.read_sql(f'''
            select distinct
            spp.creditor_no as exm_creditor_no,
            pers.sid as per_sid,
            pers.title as exm_title,
            pers.initials as exm_initials,
            pers.surname as exm_surname,
            pers.forenames as exm_forename,
            pers.email_address as exm_email
            from ar_meps_req_prd.enquiry_personnel enpe
            left join ar_meps_pan_prd.vw_delta_session_panel_positions spp
            on enpe.eper_per_sid = spp.per_sid and enpe.pan_sid = spp.stm_pan_sid
            left join ar_meps_peo_prd.persons pers
            on spp.per_sid = pers.sid
            left join ar_meps_pan_prd.vw_delta_session_panels sp
            on sp.sid = enpe.pan_sid
            where sp.ses_sid in ({session_id})
            and pers.forenames is not null
                                ''', conn)

    rolling_insert = []
    def insert_to_model(row):
        rolling_insert.append(
            UniqueCreditor(
                exm_creditor_no = int(row['exm_creditor_no']),
                per_sid = int(row['per_sid']),
                exm_title = row['exm_title'],
                exm_initials = row['exm_initials'],
                exm_surname = row['exm_surname'],
                exm_forename = row['exm_forename'],
                exm_email = row['exm_email'],
            )
        )

    df.apply(insert_to_model, axis=1)
    UniqueCreditor.objects.bulk_create(rolling_insert,update_conflicts=True,unique_fields=['exm_creditor_no'],
                                              update_fields=['per_sid','exm_title','exm_initials','exm_surname','exm_forename','exm_email']
                                              )
    
    print("UC loaded:" + str(datetime.datetime.now()))
    EarServerSettings.objects.update(delta_load_status='Table 8 of 15 loaded, Unique Creditors')


    # Get datalake data - Enquiry Personnel
    with pyodbc.connect("DSN=Impala DL", autocommit=True) as conn:
        df = pd.read_sql(f'''
            select distinct 
            cast(enpe.sid as int) as enpe_sid,
            enpe.pan_sid as sp_sid,
            enpe.eper_per_sid as per_sid
            from ar_meps_req_prd.enquiry_personnel enpe
            left join ar_meps_pan_prd.vw_delta_session_panel_positions spp
            on enpe.eper_per_sid = spp.per_sid and enpe.pan_sid = spp.stm_pan_sid
            left join ar_meps_peo_prd.persons pers
            on spp.per_sid = pers.sid
            left join ar_meps_pan_prd.vw_delta_session_panels sp
            on sp.sid = enpe.pan_sid
            where sp.ses_sid in ({session_id})
            and pers.forenames is not null
                                ''', conn)
        for examiner in EnquiryPersonnel.objects.all():
            enpe = int(examiner.enpe_sid)
            df_row = df[df.enpe_sid == enpe]
            try:
                valid_enpe = int(df_row['enpe_sid'].values[0])
                examiner.currently_valid = True
                examiner.save()
            except:
                examiner.currently_valid = False
                examiner.save()

    rolling_insert = []
    def insert_to_model(row):
        rolling_insert.append(
            EnquiryPersonnel(
                    enpe_sid = int(row['enpe_sid']),
                    sp_sid = int(row['sp_sid']),
                    per_sid_id = int(row['per_sid'])
            )
        )

    df.apply(insert_to_model, axis=1)
    EnquiryPersonnel.objects.bulk_create(rolling_insert,update_conflicts=True,unique_fields=['enpe_sid'],
                                              update_fields=['sp_sid','per_sid']
                                              )



    print("EPNE loaded:" + str(datetime.datetime.now()))
    EarServerSettings.objects.update(delta_load_status='Table 9 of 15 loaded, Enquiry Personnel')


    # Get datalake data - Enquiry Personnel - Extended
    with pyodbc.connect("DSN=Impala DL", autocommit=True) as conn:
        df = pd.read_sql(f'''
                select distinct
                enpe.sid as enpe_sid,
                sp.sid as sp_sid,
                csce.ass_code as ass_code,
                csce.com_id as com_id,
                sp.name as sp_name,
                sp.ses_sid as sp_ses_sid,
                sp.use_esm_ind as sp_use_esm_ind,
                sp.ses_sid as session,
                spp.creditor_no as exm_creditor_no,
                spp.examiner_no as exm_examiner_no,
                spp.sid as spp_sid,
                enpe.approval_ind as ear_approval_ind,
                sdc.panel_size as panel_size
                from ar_meps_req_prd.enquiry_personnel enpe
                left join ar_meps_pan_prd.vw_delta_session_panel_positions spp
                on enpe.eper_per_sid = spp.per_sid and enpe.pan_sid = spp.stm_pan_sid
                left join  ar_meps_pan_prd.vw_delta_session_panels sp
                on sp.sid = spp.stm_pan_sid
                left join (select stm_pan_sid, count(*) as panel_size from ar_meps_pan_prd.session_panel_positions spp where spp.creditor_no is not null
                group by stm_pan_sid) sdc
                on sdc.stm_pan_sid = spp.stm_pan_sid
                left join ar_meps_ord_prd.centre_sess_comp_entries csce
                on sp.sid = csce.pan_sid
                where csce.ass_code is not null and
                sp.ses_sid in({session_id}) 
                                ''', conn)

    rolling_insert = []
    def insert_to_model(row):
        rolling_insert.append(
            EnquiryPersonnelDetails(
                enpe_sid_id = int(row['enpe_sid']),
                sp_sid = int(row['sp_sid']),
                ass_code = row['ass_code'],
                com_id = row['com_id'],
                sp_name = row['sp_name'][:100],
                sp_ses_sid = int(row['sp_ses_sid']),
                sp_use_esm_ind = row['sp_use_esm_ind'],
                session = int(row['session']),
                exm_creditor_no = int(row['exm_creditor_no']),
                exm_examiner_no = row['exm_examiner_no'],
                spp_sid = int(row['spp_sid']),
                ear_approval_ind = row['ear_approval_ind'],
                panel_size = row['panel_size'],
                #panel_id_id = ExaminerPanels.objects.get(ass_code=row['ass_code'],com_id=row['com_id']) NEED TO DO THIS IN PANDAS
            )
        )

    df.apply(insert_to_model, axis=1)
    EnquiryPersonnelDetails.objects.all().delete()
    EnquiryPersonnelDetails.objects.bulk_create(rolling_insert)


    print("ECEC loaded:" + str(datetime.datetime.now()))
    EarServerSettings.objects.update(delta_load_status='Table 12 of 15 loaded, Enquiry Component Examiner Checks')


    end_time = datetime.datetime.now()
    print(end_time - start_time)


load_core_tables()
