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

from enquiries.models import CentreEnquiryRequests, EnquiryRequestParts, EnquiryComponents, EnquiryPersonnel, EnquiryPersonnelDetails, EnquiryBatches, EnquiryComponentElements, TaskManager, UniqueCreditor, EnquiryComponentsHistory, EnquiryComponentsExaminerChecks, TaskTypes, EarServerSettings, EnquiryGrades, EnquiryDeadline, ExaminerPanels, MarkTolerances, ScaledMarks, CentreEnquiryRequestsExtra, EnquiryRequestPartsExtra, EnquiryComponentsExtra

def load_core_tables():

    start_time = datetime.datetime.now()
    print("Start Time:" + str(datetime.datetime.now()))

    #Limits enquiries to session or enquiry list
    session_id = EarServerSettings.objects.first().session_id_list
    enquiry_id_list = EarServerSettings.objects.first().enquiry_id_list
    if enquiry_id_list != '':
        enquiry_id_list = ' and sid in (' + enquiry_id_list + ')'

    print("ENQ:" + enquiry_id_list)

    # Get datalake data - Enquiry Personnel - Extended
    with pyodbc.connect("DSN=hive.ucles.internal", autocommit=True) as conn:
        df = pd.read_sql(f'''
                    SELECT distinct
                    cer.sid as cer_sid,
                    ec.sid as ec_sid,
                    wrm.ses_sid as eps_ses_id,
                    wrm.ass_code as eps_ass_code,
                    wrm.com_id as eps_com_id,
                    wrm.cnu_id as eps_cnu_iYd,
                    wrm.cand_no as eps_cand_no,
                    spp.examiner_no as exm_position,
                    wrm.kbr_code as kbr_code,
                    kbr.reason as kbr_reason
                    from ar_meps_req_prd.enquiry_components ec
                    left join ar_meps_req_prd.enquiry_request_parts erp
                    on erp.sid = ec.erp_sid
                    left join ar_meps_req_prd.centre_enquiry_requests cer
                    on cer.sid = erp.cer_sid
                    left join (select ses_sid,ass_code,com_id,cnu_id,cand_no,kbr_code,mark,spp_sid from ar_meps_mark_prd.working_raw_marks where ses_sid in ({session_id}) 
                    union select ses_sid,ass_code,com_id,cnu_id,cand_no,kbr_code,mark,spp_sid from ar_meps_mark_prd.historical_raw_marks where ses_sid in ({session_id})) wrm
                    on wrm.ses_sid = ec.ccm_ses_sid
                    and wrm.ass_code = ec.ccm_ass_code
                    and wrm.com_id = ec.ccm_com_id
                    and wrm.cand_no = ec.ccm_cand_no
                    and wrm.cnu_id = ec.ccm_cnu_id
                    left join ar_meps_pan_prd.session_panel_positions spp
                    on wrm.spp_sid = spp.sid
                    left join ar_meps_mark_prd.keyed_batch_reason kbr
                    on kbr.code = wrm.kbr_code
                    where wrm.kbr_code in ('TL','GR')
                    and ec.ccm_ses_sid in ({session_id}) 
                                ''', conn)

    def insert_to_model_enpee(row):
        if EnquiryComponentsExaminerChecks.objects.filter(ec_sid=row['ec_sid']).exists():
            EnquiryComponentsExaminerChecks.objects.filter(ec_sid=row['ec_sid']).update(
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

        else:
            try:
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
            except:
                pass
        
    df.apply(insert_to_model_enpee, axis=1)

    print("EPNE2 loaded:" + str(datetime.datetime.now()))


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

    for enquiry in CentreEnquiryRequests.objects.all():
        erp_service = EnquiryRequestParts.objects.filter(cer_sid = enquiry.enquiry_id).first().service_code
        if 'P' in erp_service:
            deadline = enquiry.eps_creation_date + datetime.timedelta(days=18)
        else:
            deadline = enquiry.eps_creation_date + datetime.timedelta(days=30)
        if not EnquiryDeadline.objects.filter(enquiry_id=enquiry).exists():
            EnquiryDeadline.objects.create(
                enquiry_id = enquiry,
                enquiry_deadline = deadline,
                original_enquiry_deadline = deadline
            )

    print("ED loaded:" + str(datetime.datetime.now()))


    filename=os.path.join("Y:\Operations\Results Team\Enquiries About Results\\0.Nova Downloads\\Tolerances.xlsx")
    workbook = load_workbook(filename)
    sheet = workbook.active

    # Iterating through All rows with all columns...
    for i in range(1, sheet.max_row+1):
        row = [cell.value for cell in sheet[i]] # sheet[n] gives nth row (list of cells)
        if MarkTolerances.objects.filter(eps_ass_code = row[0],eps_com_id = row[1]).exists():
            MarkTolerances.objects.filter(eps_ass_code = row[0],eps_com_id = row[1]).update(mark_tolerance = row[2])
        else: 
            MarkTolerances.objects.create(
                eps_ass_code = row[0],
                eps_com_id = row[1],
                mark_tolerance = row[2]
            )
        
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
        
        inner join 
        (select * from ar_meps_req_prd.centre_enquiry_requests cer
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

    for enquiry in CentreEnquiryRequests.objects.all():
        enquiry_id = enquiry.enquiry_id
        if not TaskManager.objects.filter(enquiry_id=enquiry_id,task_id_id = 'INITCH').exists():
            TaskManager.objects.create(
                enquiry_id = CentreEnquiryRequests.objects.only('enquiry_id').get(enquiry_id=enquiry_id),
                ec_sid = None,
                task_id = TaskTypes.objects.get(task_id = 'INITCH'),
                task_assigned_to = None,
                task_assigned_date = None,
                task_completion_date = None
            )

    print("IEC loaded:" + str(datetime.datetime.now()))



### LOAD EXTRAS DATA

    
    # # Get datalake data - Centre Enquiry Requests
    with pyodbc.connect("DSN=hive.ucles.internal", autocommit=True) as conn:
        df = pd.read_sql(f'''
            select distinct
            cer.sid as enquiry_id,
            cer.status as enquiry_status,
            cer.created_datetime as eps_creation_date,
            cer.completed_datetime as eps_completion_date,
            cer.acknowledge_letter_ind as eps_ack_letter_ind,
            cer.ses_sid as eps_ses_sid,
            cer.cnu_id as centre_id,
            cer.created_by as created_by,
            cer.cie_direct_id as cie_direct_id
            from ar_meps_req_prd.centre_enquiry_requests cer
            left join ar_meps_req_prd.enquiry_request_parts erp
            on erp.cer_sid = cer.sid
            where ses_sid in ({session_id}) 
            and erp.es_service_code not in ('1','1S','2','2P','2PS','2S')
            {enquiry_id_list}
                                ''', conn)
        print(df)
    
    def insert_to_model_cer(row):
        if CentreEnquiryRequestsExtra.objects.filter(enquiry_id=row['enquiry_id']).exists():
            CentreEnquiryRequestsExtra.objects.filter(enquiry_id=row['enquiry_id']).update(
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
        else:
            CentreEnquiryRequestsExtra.objects.create(
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

    df.apply(insert_to_model_cer, axis=1)
    print("CER loaded:" + str(datetime.datetime.now()))

    # # Get datalake data - Enquiry Request Parts
    with pyodbc.connect("DSN=hive.ucles.internal", autocommit=True) as conn:
        df = pd.read_sql(f'''
            select 
            erp.sid as erp_sid,
            erp.cer_sid as cer_sid,
            erp.es_service_code as service_code,
            erp.caom_ses_sid as eps_ses_sid,
            erp.caom_ass_code as eps_ass_code,
            erp.caom_asv_ver_no as eps_ass_ver_no,
            erp.caom_opt_code as eps_option_code,
            erp.caom_can_unique_identifier as eps_cand_unique_id,
            erp.caom_cand_no as eps_cand_id,
            erp.caom_cnu_id as eps_centre_id,
            if(erp.component_ind="Y","C","S") as eps_comp_ind,
            erp.caom_measure as eps_script_measure,
            erp.booked_in_error_ind as booked_in_error_ind,
            can.full_name as stud_name
            from ar_meps_req_prd.enquiry_request_parts erp
            left join cie.ca_candidates can
            on erp.caom_can_unique_identifier = can.unique_id
            where caom_ses_sid in ({session_id}) 
                                ''', conn)

    def insert_to_model_erp(row):
        if EnquiryRequestPartsExtra.objects.filter(erp_sid = row['erp_sid']).exists():
            EnquiryRequestPartsExtra.objects.filter(erp_sid = row['erp_sid']).update(
                erp_sid = row['erp_sid'],
                cer_sid = CentreEnquiryRequestsExtra.objects.only('enquiry_id').get(enquiry_id=row['cer_sid']),
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
                stud_name = row['stud_name'],
        )
        else:
            try:
                EnquiryRequestPartsExtra.objects.create(
                    erp_sid = row['erp_sid'],
                    cer_sid = CentreEnquiryRequestsExtra.objects.only('enquiry_id').get(enquiry_id=row['cer_sid']),
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
                    stud_name = row['stud_name'],
                )
            except:
                pass

    df.apply(insert_to_model_erp, axis=1)


    print("ERP loaded:" + str(datetime.datetime.now()))

    # # Get datalake data - Enquiry Components
    with pyodbc.connect("DSN=hive.ucles.internal", autocommit=True) as conn:
        df = pd.read_sql(f'''
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
                ec.ccm_measure as ccm_measure
                from ar_meps_req_prd.enquiry_components ec
                left join ar_meps_req_prd.enquiry_request_parts erp
                on ec.erp_sid = erp.sid
                left join cie.ca_products prod
                on ec.ccm_ass_code = prod.assessment
                and ec.ccm_asv_ver_no = prod.assessment_version_no
                and ec.ccm_com_id = prod.component
                and erp.caom_opt_code = prod.option_code
                left join cie.ods_sessions ses
                on ec.ccm_ses_sid = ses.sessionid
                where ccm_ses_sid in ({session_id}) 
                                ''', conn)

    def insert_to_model_ec(row):
        if EnquiryComponentsExtra.objects.filter(ec_sid = row['ec_sid']).exists():
            EnquiryComponentsExtra.objects.filter(ec_sid = row['ec_sid']).update(
                ec_sid = row['ec_sid'],
                erp_sid = EnquiryRequestPartsExtra.objects.only('erp_sid').get(erp_sid=row['erp_sid']),
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
            )
        else:
            try:
                EnquiryComponentsExtra.objects.create(
                    ec_sid = row['ec_sid'],
                    erp_sid = EnquiryRequestPartsExtra.objects.only('erp_sid').get(erp_sid=row['erp_sid']),
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
                )
            except:
                pass
    
    df.apply(insert_to_model_ec, axis=1)

    filename=os.path.join("Y:\Operations\Results Team\Enquiries About Results\\0.Nova Downloads\\Type Of Script.xlsx")
    workbook = load_workbook(filename)
    sheet = workbook.active

    for row in sheet.iter_rows():
        ass_code = str(row[0].value).zfill(4)
        comp_id = row[2].value
        script_type = row[5].value

        EnquiryComponentsExtra.objects.filter(eps_ass_code=ass_code,eps_com_id=comp_id).update(script_type=script_type)


    print("EC loaded:" + str(datetime.datetime.now()))




    end_time = datetime.datetime.now()
    print(end_time - start_time)

load_core_tables()
