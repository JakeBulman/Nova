import pandas as pd
import pyodbc

import sys
import os
import django
import datetime
from django.utils import timezone

#Limits enquiries to only non-completed
temp_filter = 1


sys.path.append('C:/Dev/redepplan')
os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings'
django.setup()
from enquiries.models import CentreEnquiryRequests, EnquiryComponentsHistory, EnquiryComponents, EnquiryComponentsExaminerChecks

EnquiryComponentsHistory.objects.all().delete()
EnquiryComponentsExaminerChecks.objects.all().delete()

def load_core_tables():

    start_time = datetime.datetime.now()
    print("Start Time:" + str(datetime.datetime.now()))

    # Get datalake data - ECH
    with pyodbc.connect("DSN=hive.ucles.internal", autocommit=True) as conn:
        df = pd.read_sql('''
                        SELECT distinct
                        cer.sid as cer_sid,
                        ec.sid as ec_sid,
                        wrm.ses_sid as ses_sid,
                        wrm.ass_code as ass_code,
                        wrm.com_id as com_id,
                        wrm.cnu_id as cnu_id,
                        wrm.cand_no as cand_no,
                        spp.examiner_no as exm_position,
                        wrm.kbr_code as kbr_code,
                        kbr.reason as kbr_reason,
                        wrm.mark as current_mark,
                        ec.ccm_measure as ear_mark,
                        ec.ccm_outcome as ear_mark_alt
                        from ar_meps_req_prd.enquiry_components ec
                        left join ar_meps_req_prd.enquiry_request_parts erp
                        on erp.sid = ec.erp_sid
                        left join ar_meps_req_prd.centre_enquiry_requests cer
                        on cer.sid = erp.cer_sid
                        left join ar_meps_mark_prd.working_raw_marks wrm
                        on wrm.ses_sid = ec.ccm_ses_sid
                        and wrm.ass_code = ec.ccm_ass_code
                        and wrm.com_id = ec.ccm_com_id
                        and wrm.cand_no = ec.ccm_cand_no
                        and wrm.cnu_id = ec.ccm_cnu_id
                        left join ar_meps_pan_prd.session_panel_positions spp
                        on wrm.spp_sid = spp.sid
                        left join ar_meps_mark_prd.keyed_batch_reason kbr
                        on kbr.code = wrm.kbr_code
                        where ec.ccm_ses_sid = 19646

                        ''', conn)

    def insert_to_model_enpee(row):
        #try:
            EnquiryComponentsHistory.objects.create(
            cer_sid = CentreEnquiryRequests.objects.only('enquiry_id').get(enquiry_id=row['cer_sid']),
            ec_sid = EnquiryComponents.objects.only('ec_sid').get(ec_sid=row['ec_sid']),
            eps_ses_sid = row['ses_sid'],
            eps_ass_code = row['ass_code'],
            eps_com_id = row['com_id'],
            eps_cnu_id = row['cnu_id'],
            eps_cand_no = row['cand_no'],
            exm_position = row['exm_position'],
            kbr_code = row['kbr_code'],
            kbr_reason = row['kbr_reason'],
            current_mark = row['current_mark'],
            ear_mark = row['ear_mark'],
            ear_mark_alt = row['ear_mark_alt'],
            )
        #except:
        #    pass
        
    df.apply(insert_to_model_enpee, axis=1)

    print("ECH loaded:" + str(datetime.datetime.now()))


    # Get datalake data - Enquiry Personnel - Extended
    with pyodbc.connect("DSN=hive.ucles.internal", autocommit=True) as conn:
        df = pd.read_sql('''
                    SELECT distinct
                    cer.sid as cer_sid,
                    ec.sid as ec_sid,
                    wrm.ses_sid as eps_ses_id,
                    wrm.ass_code as eps_ass_code,
                    wrm.com_id as eps_com_id,
                    wrm.cnu_id as eps_cnu_id,
                    wrm.cand_no as eps_cand_no,
                    spp.examiner_no as exm_position,
                    wrm.kbr_code as kbr_code,
                    kbr.reason as kbr_reason
                    from ar_meps_req_prd.enquiry_components ec
                    left join ar_meps_req_prd.enquiry_request_parts erp
                    on erp.sid = ec.erp_sid
                    left join ar_meps_req_prd.centre_enquiry_requests cer
                    on cer.sid = erp.cer_sid
                    left join (select ses_sid,ass_code,com_id,cnu_id,cand_no,kbr_code,mark,spp_sid from ar_meps_mark_prd.working_raw_marks where ses_sid = 19646 
                    union select ses_sid,ass_code,com_id,cnu_id,cand_no,kbr_code,mark,spp_sid from ar_meps_mark_prd.historical_raw_marks where ses_sid = 19646) wrm
                    on wrm.ses_sid = ec.ccm_ses_sid
                    and wrm.ass_code = ec.ccm_ass_code
                    and wrm.com_id = ec.ccm_com_id
                    and wrm.cand_no = ec.ccm_cand_no
                    and wrm.cnu_id = ec.ccm_cnu_id
                    left join ar_meps_pan_prd.session_panel_positions spp
                    on wrm.spp_sid = spp.sid
                    left join ar_meps_mark_prd.keyed_batch_reason kbr
                    on kbr.code = wrm.kbr_code
                    where ec.ccm_ses_sid = 19646
                    and wrm.kbr_code in ('TL','GR')
                        ''', conn)

    def insert_to_model_enpee(row):
        #try:
            EnquiryComponentsExaminerChecks.objects.create(
            cer_sid = CentreEnquiryRequests.objects.only('enquiry_id').get(enquiry_id=row['cer_sid']),
            ec_sid = EnquiryComponents.objects.only('ec_sid').get(ec_sid=row['ec_sid']),
            eps_ses_sid = row['eps_ses_id'],
            eps_ass_code = row['eps_ass_code'],
            eps_com_id = row['eps_com_id'],
            eps_cnu_id = row['eps_cnu_id'],
            eps_cand_no = row['eps_cand_no'],
            exm_position = row['exm_position'],
            kbr_code = row['kbr_code'],
            kbr_reason = row['kbr_reason'],
            )
        #except:
        #    pass
        
    df.apply(insert_to_model_enpee, axis=1)

    print("EPNE2 loaded:" + str(datetime.datetime.now()))

    end_time = datetime.datetime.now()
    print(end_time - start_time)

load_core_tables()
