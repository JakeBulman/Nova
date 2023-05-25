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
from enquiries.models import CentreEnquiryRequests, EnquiryRequestParts, EnquiryComponents, EnquiryPersonnel, EnquiryPersonnelDetails, EnquiryBatches, EnquiryComponentElements, TaskManager, UniqueCreditor, ScriptApportionment

def clear_tables():
    CentreEnquiryRequests.objects.all().delete()
    #Cascades to EnquiryRequestParts, EnquiryComponents, EnquiryComponentElements

    TaskManager.objects.all().delete()

    EnquiryBatches.objects.all().delete()

    UniqueCreditor.objects.all().delete()
    #Cascades to EnquiryPersonnel, EnquiryPersonnelDetails

    TaskManager.objects.all().delete()
    ScriptApportionment.objects.all().delete()

    print('Tables Cleared')

clear_tables()

def load_core_tables():

    start_time = datetime.datetime.now()
    print("Start Time:" + str(datetime.datetime.now()))


    # # Get datalake data - Centre Enquiry Requests
    with pyodbc.connect("DSN=hive.ucles.internal", autocommit=True) as conn:
        df = pd.read_sql('''
            select 
            sid as enquiry_id,
            status as enquiry_status,
            created_datetime as eps_creation_date,
            completed_datetime as eps_completion_date,
            acknowledge_letter_ind as eps_ack_letter_ind,
            ses_sid as eps_ses_sid,
            cnu_id as centre_id,
            created_by as created_by,
            cie_direct_id as cie_direct_id
            from ar_meps_req_prd.centre_enquiry_requests
            where ses_sid in (19646) and sid in (
            1222128,
            1222158,
            1222300,
            1222304,
            1222322,
            1222324,
            1222326,
            1222326,
            1222338,
            1222364,
            1222370,
            1222414,
            1222414,
            1222416,
            1222416,
            1222542,
            1222588,
            1222588,
            1222634,
            1222634,
            1222636,
            1222776,
            1222776,
            1222778,
            1222778,
            1222780,
            1222780,
            1222780,
            1222782,
            1222782,
            1222784,
            1222786,
            1222798,
            1222798,
            1222800,
            1222804,
            1222808,
            1222808,
            1222810,
            1222882,
            1222882,
            1222886,
            1222892,
            1222894,
            1222894,
            1222926,
            1222928,
            1222930,
            1222930,
            1222932,
            1222934,
            1222934,
            1222934,
            1222936,
            1222938,
            1222966,
            1222972,
            1222972,
            1222988,
            1222992,
            1222992,
            1222994,
            1222994,
            1223006,
            1223006,
            1223006,
            1223008,
            1223010,
            1223018,
            1223018,
            1223020,
            1223020
            )
                                ''', conn)

    def insert_to_model_cer(row):
        CentreEnquiryRequests.objects.create(
            enquiry_id = row['enquiry_id'],
            enquiry_status = row['enquiry_status'],
            eps_creation_date = row['eps_creation_date'],
            eps_completion_date = row['eps_completion_date'],
            eps_ack_letter_ind = row['eps_ack_letter_ind'],
            eps_ses_sid = row['eps_ses_sid'],
            centre_id = row['centre_id'],
            created_by = row['created_by'],
            cie_direct_id = row['cie_direct_id'],
        )
        TaskManager.objects.create(
            enquiry_id = CentreEnquiryRequests.objects.only('enquiry_id').get(enquiry_id=row['enquiry_id']),
            ec_sid = None,
            task_id = 'INITCH',
            task_assigned_to = None,
            task_assigned_date = None,
            task_completion_date = None
        )

    df.apply(insert_to_model_cer, axis=1)
    print("CER loaded:" + str(datetime.datetime.now()))

    # # Get datalake data - Enquiry Request Parts
    with pyodbc.connect("DSN=hive.ucles.internal", autocommit=True) as conn:
        df = pd.read_sql('''
            select 
            sid as erp_sid,
            cer_sid as cer_sid,
            es_service_code as service_code,
            caom_ses_sid as eps_ses_sid,
            caom_ass_code as eps_ass_code,
            caom_asv_ver_no as eps_ass_ver_no,
            caom_opt_code as eps_option_code,
            caom_can_unique_identifier as eps_cand_unique_id,
            caom_cand_no as eps_cand_id,
            caom_cnu_id as eps_centre_id,
            if(component_ind="Y","C","S") as eps_comp_ind,
            caom_measure as eps_script_measure,
            booked_in_error_ind as booked_in_error_ind
            from ar_meps_req_prd.enquiry_request_parts
            where caom_ses_sid in (19646) 
                                ''', conn)

    def insert_to_model_erp(row):
        try:
            EnquiryRequestParts.objects.create(
                erp_sid = row['erp_sid'],
                cer_sid = CentreEnquiryRequests.objects.only('enquiry_id').get(enquiry_id=row['cer_sid']),
                service_code = row['service_code'],
                eps_ses_sid = row['eps_ses_sid'],
                eps_ass_code = row['eps_ass_code'],
                eps_ass_ver_no = row['eps_ass_ver_no'],
                eps_option_code = row['eps_option_code'],
                eps_cand_unique_id = row['eps_cand_unique_id'],
                eps_cand_id = row['eps_cand_id'],
                eps_centre_id = row['eps_centre_id'],
                eps_comp_ind = row['eps_comp_ind'],
                eps_script_measure = row['eps_script_measure'],
                booked_in_error_ind = row['booked_in_error_ind'],
        )
        except:
            pass

    df.apply(insert_to_model_erp, axis=1)


    print("ERP loaded:" + str(datetime.datetime.now()))

    # # Get datalake data - Enquiry Components
    with pyodbc.connect("DSN=hive.ucles.internal", autocommit=True) as conn:
        df = pd.read_sql('''
                select distinct
                ec.sid as ec_sid,
                ec.erp_sid as erp_sid,
                ec.ccm_ses_sid as eps_ses_sid,
                ses.sessionname as eps_ses_name,
                ec.ccm_ass_code as eps_ass_code,
                ec.ccm_asv_ver_no as eps_ass_ver_no,
                ec.ccm_com_id as eps_com_id,
                prod.qualfication as eps_qual_id,
                prod.qualification_short_text as eps_qual_name,
                prod.assessment_short_text as eps_ass_name,
                prod.component_text as eps_comp_name,
                ec.ccm_measure as ccm_measure,
                can.stud_name as stud_name
                from ar_meps_req_prd.enquiry_components ec
                left join cie.ca_products prod
                on ec.ccm_ass_code = prod.assessment
                and ec.ccm_asv_ver_no = prod.assessment_version_no
                and ec.ccm_com_id = prod.component
                left join cie.ods_sessions ses
                on ec.ccm_ses_sid = ses.sessionid
                left join (select distinct ses_id, cand_ses_id, stud_name from cie.ca_entries) can
                on ec.ccm_ses_sid = can.ses_id
                and ec.ccm_cand_no = can.cand_ses_id
                where ccm_ses_sid in (19646) 
                                ''', conn)

    def insert_to_model_ec(row):
        try:
            EnquiryComponents.objects.create(
                ec_sid = row['ec_sid'],
                erp_sid = EnquiryRequestParts.objects.only('erp_sid').get(erp_sid=row['erp_sid']),
                eps_ses_sid = row['eps_ses_sid'],
                eps_ses_name = row['eps_ses_name'],
                eps_ass_code = row['eps_ass_code'],
                eps_ass_ver_no = row['eps_ass_ver_no'],
                eps_com_id = row['eps_com_id'],
                eps_qual_id = row['eps_qual_id'],
                eps_qual_name = row['eps_qual_name'],
                eps_ass_name = row['eps_ass_name'],
                eps_comp_name = row['eps_comp_name'],
                ccm_measure = row['ccm_measure'],
                stud_name = row['stud_name'],
            )
        except Exception:
            pass
    
    df.apply(insert_to_model_ec, axis=1)

    print("EC loaded:" + str(datetime.datetime.now()))

    # # Get datalake data - Enquiry Batches
    with pyodbc.connect("DSN=hive.ucles.internal", autocommit=True) as conn:
        df = pd.read_sql('''
            select distinct
            sb.sid as eb_sid,
            sb.created_date as created_date,
            sb.enpe_eper_per_sid as eper_per_sid
            from ar_meps_req_prd.summary_batches sb
            left join ar_meps_req_prd.enquiry_component_elements ece
            on sb.sid = ece.eb_sid
            left join ar_meps_req_prd.enquiry_components ec
            on ec.sid = ece.ec_sid
            where ec.ccm_ses_sid in (19646) 
                                ''', conn)

    def insert_to_model_eb(row):
        EnquiryBatches.objects.create(
            eb_sid = row['eb_sid'],
            created_date = row['created_date'],
            enpe_eper_per_sid = row['eper_per_sid'],
        )

    df.apply(insert_to_model_eb, axis=1)
    print("EB loaded:" + str(datetime.datetime.now()))

    #Get datalake data - Enquiry Components
    with pyodbc.connect("DSN=hive.ucles.internal", autocommit=True) as conn:
        df = pd.read_sql('''
            select distinct
            ece.ec_sid as ec_sid,
            ece.status as ece_status,
            ece.eb_sid as eb_sid,
            ece.clerical_mark as clerical_mark,
            ece.mark_after_enquiry as mark_after_enquiry,
            ece.justification_code as justification_code
            from  ar_meps_req_prd.enquiry_component_elements ece
            left join ar_meps_req_prd.enquiry_components ec
            on ece.ec_sid = ec.sid
            where ec.ccm_ses_sid in (19646) 
                                ''', conn)

    def insert_to_model_ec(row):
        try:
            EnquiryComponentElements.objects.create(
                ec_sid = EnquiryComponents.objects.only('ec_sid').get(ec_sid=row['ec_sid']),
                ece_status = row['ece_status'],
                eb_sid = EnquiryBatches.objects.only('eb_sid').filter(eb_sid=row['eb_sid']).first(),
                clerical_mark = row['clerical_mark'],
                mark_after_enquiry = row['mark_after_enquiry'],
                justification_code = row['justification_code'],
            )
        except Exception:
            pass    


    df.apply(insert_to_model_ec, axis=1)

    print("ECE loaded:" + str(datetime.datetime.now()))




    # Get datalake data - Unique Creditors
    with pyodbc.connect("DSN=hive.ucles.internal", autocommit=True) as conn:
        df = pd.read_sql('''
            select distinct
            spp.creditor_no as exm_creditor_no,
            per.sid as per_sid,
            per.title as exm_title,
            per.initials as exm_initials,
            per.surname as exm_surname,
            per.forenames as exm_forename,
            per.email_address as exm_email
            from ar_meps_req_prd.enquiry_personnel enpe
            left join ar_meps_pan_prd.session_panel_positions spp
            on enpe.eper_per_sid = spp.per_sid and enpe.pan_sid = spp.stm_pan_sid
            inner join (select z.stm_pan_sid, z.creditor_no, max(z.load_date) as max_date from ar_meps_pan_prd.session_panel_positions z group by z.stm_pan_sid, z.creditor_no) mld
            on spp.stm_pan_sid = mld.stm_pan_sid and spp.creditor_no = mld.creditor_no and spp.load_date = mld.max_date
            left join cie.vw_persons per
            on spp.per_sid = per.sid
            left join ar_meps_pan_prd.session_panels sp
            on sp.sid = enpe.pan_sid
            where sp.ses_sid in (19646) 
                                ''', conn)

    def insert_to_model_enpe(row):
        UniqueCreditor.objects.create(
            exm_creditor_no = row['exm_creditor_no'],
            per_sid = row['per_sid'],
            exm_title = row['exm_title'],
            exm_initials = row['exm_initials'],
            exm_surname = row['exm_surname'],
            exm_forename = row['exm_forename'],
            exm_email = row['exm_email'],
        )

    df.apply(insert_to_model_enpe, axis=1)
    print("UC loaded:" + str(datetime.datetime.now()))



    # Get datalake data - Enquiry Personnel
    with pyodbc.connect("DSN=hive.ucles.internal", autocommit=True) as conn:
        df = pd.read_sql('''
            select distinct 
            enpe.sid as enpe_sid,
            enpe.pan_sid as sp_sid,
            enpe.eper_per_sid as per_sid
            from ar_meps_req_prd.enquiry_personnel enpe
            left join ar_meps_pan_prd.session_panels sp
            on sp.sid = enpe.pan_sid
            where sp.ses_sid in (19646) 
                                ''', conn)

    def insert_to_model_enpe(row):
        try:
            EnquiryPersonnel.objects.create(
                enpe_sid = row['enpe_sid'],
                sp_sid = row['sp_sid'],
                per_sid = UniqueCreditor.objects.only('per_sid').get(per_sid=row['per_sid']),
            )
        except:
            pass
    
    df.apply(insert_to_model_enpe, axis=1)

    print("EPNE loaded:" + str(datetime.datetime.now()))


    # Get datalake data - Enquiry Personnel - Extended
    with pyodbc.connect("DSN=hive.ucles.internal", autocommit=True) as conn:
        df = pd.read_sql('''
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
                sp.ses_sid in (19646) 
                                ''', conn)

    def insert_to_model_enpee(row):
        try:
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
            )
        except:
            pass
    
    df.apply(insert_to_model_enpee, axis=1)

    print("EPNE2 loaded:" + str(datetime.datetime.now()))

    end_time = datetime.datetime.now()
    #print(end_time - start_time)

load_core_tables()
