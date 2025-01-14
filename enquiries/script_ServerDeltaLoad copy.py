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


start_time = datetime.datetime.now()
print("Start Time:" + str(datetime.datetime.now()))

#Limits enquiries to session or enquiry list
session_id = EarServerSettings.objects.first().session_id_list
enquiry_id_list = EarServerSettings.objects.first().enquiry_id_list
if enquiry_id_list != '':
    enquiry_id_list = ' and cer.sid in (' + enquiry_id_list + ')'


    # # Get datalake data - Scaled Marks
with pyodbc.connect("DSN=Impala DL", autocommit=True) as conn:
    df = pd.read_sql(f'''
    select 
    distinct 
        c.sessionassessmentcomponentid,
        a.assessmentcode as eps_ass_code,
        a.componentid as eps_com_id,
        c.centrenumber as eps_cnu_id,
        c.candidatenumber as eps_cand_no,
        s.sessionid as eps_ses_id,
        c.mark as raw_mark,
        c.assessormark as assessor_mark,
        c.finalmark as final_mark,
        c.examinernumber as exm_examiner_no,
        case
        when c.assessormark is not null then assessormark 
        else c.mark
        end as scaled_mark,
        case
        when assessormark is not null then "Scaled" 
        when assessormark is null then "No scaling"
        end as original_exm_scaled
    from cie.ods_candidatemarkelementmarks as c
    left join cie.ods_sessionassessmentcomponents as s
    on c.sessionassessmentcomponentid=s.sessionassessmentcomponentid
    left join cie.ods_assessmentcomponents as a
    on s.assessmentcomponentid=a.assessmentcomponentid

    inner join 
    (select 
    cer.cnu_id,
    ec.ccm_ass_code,
    ec.ccm_com_id,
    erp.caom_cand_no,
    cer.ses_sid
    from ar_meps_req_prd.centre_enquiry_requests cer
    left join ar_meps_req_prd.enquiry_request_parts erp
    on cer.sid=erp.cer_sid
    left join ar_meps_req_prd.enquiry_components ec
    on erp.sid=ec.erp_sid
    ) req
    on req.cnu_id = c.centrenumber
    and req.ccm_ass_code = a.assessmentcode
    and req.ccm_com_id = a.componentid
    and req.caom_cand_no = c.candidatenumber
    and req.ses_sid = s.sessionid
    
    where c.businessstreamid='02'
        and s.isdeletedfromsource!=1
        and c.isdeletedfromsource!=1
        and a.isdeletedfromsource!=1
        and c.examinernumber!=''
        and s.sessionid in ({session_id}) 
                            ''', conn)
    
rolling_insert = []
def insert_to_model(row):
    rolling_insert.append(
    ScaledMarks(
        eps_ass_code = str(row['eps_ass_code']).zfill(4),
        eps_com_id = str(int(row['eps_com_id'])).zfill(2),
        eps_cnu_id = row['eps_cnu_id'],
        eps_cand_no = row['eps_cand_no'],
        eps_ses_sid = row['eps_ses_id'],
        raw_mark = row['raw_mark'],
        assessor_mark  = row['assessor_mark'],
        final_mark = row['final_mark'],
        exm_examiner_no = row['exm_examiner_no'],
        scaled_mark = row['scaled_mark'],
        original_exm_scaled = row['original_exm_scaled'],
        )
    )

df.apply(insert_to_model, axis=1)
print("Scaled Marks prepped:" + str(datetime.datetime.now())) 
ScaledMarks.objects.all().delete()
print("Scaled Marks deleted:" + str(datetime.datetime.now()))
ScaledMarks.objects.bulk_create(rolling_insert)
print("Scaled Marks loaded:" + str(datetime.datetime.now()))

