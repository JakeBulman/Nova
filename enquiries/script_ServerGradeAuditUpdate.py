import sys
import os
import django
import datetime
import pyodbc
import pandas as pd

if os.getenv('DJANGO_DEVELOPMENT') == 'true':
    path = os.path.join('C:\\Users\\bulmaj\\OneDrive - Cambridge\\Desktop\\Dev\\Nova')
    sys.path.append(path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings_dev'
else:
    sys.path.append('C:/Dev/redepplan')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings'

django.setup()

from enquiries.models import EarServerSettings, CentreEnquiryRequests, EnquiryGrades



def load_core_tables():

    #Limits enquiries to only non-completed
    session_id = EarServerSettings.objects.first().session_id_list
    enquiry_id_list = EarServerSettings.objects.first().enquiry_id_list
    if enquiry_id_list != '':
        enquiry_id_list = ' and sid in (' + enquiry_id_list + ')'



    # # Get datalake data - Enquiry Request Parts
    with pyodbc.connect("DSN=hive.ucles.internal", autocommit=True) as conn:
        df = pd.read_sql(f'''
            select 
            cer.sid as enquiry_id,
            erp.caom_ass_code as eps_ass_code,
            erp.caom_cand_no as eps_cand_no,
            qgrp.title as previous_grade,
            qgrp.seq_no as previous_seq,
            qgrn.title as new_grade,
            qgrn.seq_no as new_seq
                         
            from ar_meps_req_prd.centre_enquiry_requests cer
            left join ar_meps_req_prd.enquiry_request_parts erp
            on cer.sid = erp.cer_sid
            left join ar_meps_ord_prd.audit_changes ac
            on cer.ses_sid = ac.ses_sid
            and cer.cnu_id = ac.co_centre_id
            and erp.caom_ass_code = ac.ass_code
            and erp.caom_cand_no = ac.coc_cand_no
            left join ar_meps_prod_prd.qualification_grades qgr
            on qgr.qgs_sid = erp.qgr_qgs_sid and qgr.seq_no = erp.qgr_seq_no_derived
            left join ar_meps_prod_prd.qualification_grades qgrp
            on erp.qgr_qgs_sid = qgrp.qgs_sid and qgrp.seq_no = ac.previous_value
            left join ar_meps_prod_prd.qualification_grades qgrn
            on erp.qgr_qgs_sid = qgrn.qgs_sid and qgrn.seq_no = ac.new_value
            where ac.record_type = "CAOM"
            --and ac.confirmation_status = "UNC"
            and ac.field_name in ("QGR_SEQ_NO_DERIVED","QGR_SEQ_NO_MANUAL")
            and ac.ses_sid in ({session_id}) 
                                ''', conn)

    def insert_to_model_erp(row):
        if EnquiryGrades.objects.filter(enquiry_id=row['enquiry_id']).exists():
            EnquiryGrades.objects.filter(enquiry_id=row['enquiry_id']).update(
                enquiry_id = CentreEnquiryRequests.objects.only('enquiry_id').get(enquiry_id=row['enquiry_id']),
                eps_ass_code = row['eps_ass_code'],
                eps_cand_no = row['eps_cand_no'],
                previous_grade = row['previous_grade'],
                previous_seq = row['previous_seq'],
                new_grade = row['new_grade'],
                new_seq = row['new_seq']
            )
        else:
            try:
                EnquiryGrades.objects.create(
                    enquiry_id = CentreEnquiryRequests.objects.only('enquiry_id').get(enquiry_id=row['enquiry_id']),
                    eps_ass_code = row['eps_ass_code'],
                    eps_cand_no = row['eps_cand_no'],
                    previous_grade = row['previous_grade'],
                    previous_seq = row['previous_seq'],
                    new_grade = row['new_grade'],
                    new_seq = row['new_seq']
                )
            except:
                pass


    df.apply(insert_to_model_erp, axis=1)


    print("EG loaded:" + str(datetime.datetime.now()))

load_core_tables()