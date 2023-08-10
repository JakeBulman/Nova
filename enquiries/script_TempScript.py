import sys
import os
import django
import datetime
import pyodbc
import pandas as pd
from openpyxl import load_workbook


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

from enquiries.models import EnquiryPersonnelDetails, EnquiryPersonnel, ExaminerPanels, UniqueCreditor, EarServerSettings, ScaledMarks, UniqueCreditor, ExaminerAvailability, ExaminerNotes, ExaminerConflicts
from django.contrib.auth.models import User

#Limits enquiries to session or enquiry list
session_id = EarServerSettings.objects.first().session_id_list
enquiry_id_list = EarServerSettings.objects.first().enquiry_id_list
if enquiry_id_list != '':
    enquiry_id_list = ' and sid in (' + enquiry_id_list + ')'

print("ENQ:" + enquiry_id_list)



# Get datalake data - Enquiry Personnel - Extended
with pyodbc.connect("DSN=hive.ucles.internal", autocommit=True) as conn:
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
            left join ar_meps_pan_prd.session_panel_positions spp
            on enpe.eper_per_sid = spp.per_sid and enpe.pan_sid = spp.stm_pan_sid
            inner join (select z.stm_pan_sid, z.creditor_no, max(z.load_date) as max_date from ar_meps_pan_prd.session_panel_positions z group by z.stm_pan_sid, z.creditor_no) mld
            on spp.stm_pan_sid = mld.stm_pan_sid and spp.creditor_no = mld.creditor_no and spp.load_date = mld.max_date
            left join  ar_meps_pan_prd.session_panels sp
            on sp.sid = spp.stm_pan_sid
            left join (select stm_pan_sid, count(*) as panel_size from ar_meps_pan_prd.session_panel_positions spp where spp.creditor_no is not null
            group by stm_pan_sid) sdc
            on sdc.stm_pan_sid = spp.stm_pan_sid
            inner join (select z.sid, max(z.load_date) as max_date from ar_meps_pan_prd.session_panels z group by z.sid) mld2
            on sp.sid = mld2.sid and sp.load_date = mld2.max_date
            left join ar_meps_ord_prd.centre_sess_comp_entries csce
            on sp.sid = csce.pan_sid
            where 
            sp.ses_sid in({session_id}) 
            and csce.ass_code is not null
                            ''', conn)
print(df)
    
def insert_to_model_enpee(row):
    print(row['ass_code'] + row['com_id'])
    if EnquiryPersonnelDetails.objects.filter(enpe_sid=row['enpe_sid'],ass_code = row['ass_code'],com_id = row['com_id']).exists():
        EnquiryPersonnelDetails.objects.filter(enpe_sid=row['enpe_sid'],ass_code = row['ass_code'],com_id = row['com_id']).update(
            enpe_sid = EnquiryPersonnel.objects.only('enpe_sid').get(enpe_sid=row['enpe_sid']),
            sp_sid = row['sp_sid'],
            ass_code = row['ass_code'],
            com_id = row['com_id'],
            sp_name = row['sp_name'],
            sp_ses_sid = row['sp_ses_sid'],
            sp_use_esm_ind = row['sp_use_esm_ind'],
            session = row['session'],
            exm_creditor_no = row['exm_creditor_no'],
            exm_examiner_no = row['exm_examiner_no'],
            spp_sid = row['spp_sid'],
            ear_approval_ind = row['ear_approval_ind'],
            panel_size = row['panel_size'],
            panel_id = ExaminerPanels.objects.get(ass_code=row['ass_code'],com_id=row['com_id'])
        )
    else:        
        EnquiryPersonnelDetails.objects.create(
            enpe_sid = EnquiryPersonnel.objects.only('enpe_sid').get(enpe_sid=row['enpe_sid']),
            sp_sid = row['sp_sid'],
            ass_code = row['ass_code'],
            com_id = row['com_id'],
            sp_name = row['sp_name'],
            sp_ses_sid = row['sp_ses_sid'],
            sp_use_esm_ind = row['sp_use_esm_ind'],
            session = row['session'],
            exm_creditor_no = row['exm_creditor_no'],
            exm_examiner_no = row['exm_examiner_no'],
            spp_sid = row['spp_sid'],
            ear_approval_ind = row['ear_approval_ind'],
            panel_size = row['panel_size'],
            panel_id = ExaminerPanels.objects.get(ass_code=row['ass_code'],com_id=row['com_id'])
            )


df.apply(insert_to_model_enpee, axis=1)

print("EPD loaded:" + str(datetime.datetime.now()))