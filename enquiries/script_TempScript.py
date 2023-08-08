import sys
import os
import django
import datetime
import pyodbc
import pandas as pd


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

from enquiries.models import CentreEnquiryRequests, EnquiryDeadline, ExaminerPanels, UniqueCreditor, EarServerSettings, ScaledMarks

#Limits enquiries to session or enquiry list
session_id = EarServerSettings.objects.first().session_id_list
enquiry_id_list = EarServerSettings.objects.first().enquiry_id_list
if enquiry_id_list != '':
    enquiry_id_list = ' and sid in (' + enquiry_id_list + ')'

print("ENQ:" + enquiry_id_list)
# # Get datalake data - Enquiry Request Parts
with pyodbc.connect("DSN=hive.ucles.internal", autocommit=True) as conn:
    df = pd.read_sql(f'''
      select 
        c.sessionassessmentcomponentid,
        a.assessmentcode as eps_ass_code,
        a.componentid as eps_com_id,
        c.centrenumber as eps_cnu_id,
        c.candidatenumber as eps_cand_no,
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
      from cie.ods_CandidateMarkElementMarks as c
      left join cie.ods_sessionassessmentcomponents as s
      on c.sessionassessmentcomponentid=s.sessionassessmentcomponentid
      and c.sessionpartitionkey=s.sessionpartitionkey
      left join cie.ods_assessmentcomponents as a
      on s.assessmentcomponentid=a.assessmentcomponentid
      where c.businessstreamid='02'
        and s.isdeletedfromsource!=1
        and c.isdeletedfromsource!=1
        and a.isdeletedfromsource!=1
        and c.examinernumber!=''
        and s.sessionid in ({session_id}) 
                            ''', conn)

def insert_to_model_erp(row):
    try:
        ScaledMarks.objects.create(
            eps_ass_code = row['eps_ass_code'],
            eps_com_id = row['eps_com_id'],
            eps_cnu_id = row['eps_cnu_id'],
            eps_cand_no = row['eps_cand_no'],
            raw_mark = row['raw_mark'],
            assessor_mark  = row['assessor_mark'],
            final_mark = row['final_mark'],
            exm_examiner_no = row['exm_examiner_no'],
            scaled_mark = row['scaled_mark'],
            original_exm_scaled = row['original_exm_scaled'],
            )
    except:
        pass

df.apply(insert_to_model_erp, axis=1)


print("ERP loaded:" + str(datetime.datetime.now()))