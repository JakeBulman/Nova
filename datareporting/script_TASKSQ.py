import sys
import os
import django
from django.utils import timezone
import datetime
from openpyxl import load_workbook
import pyodbc
import pandas as pd
import time

start_time = time.time()

if os.getenv('DJANGO_DEVELOPMENT') == 'true':
    print('DEV')
    path = os.path.join('C:\\Users\\bulmaj\\OneDrive - Cambridge\\Desktop\\Dev\\Nova')
    sys.path.append(path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings_dev'
elif os.getenv('DJANGO_DEVELOPMENT2') == 'true':
    print('DEV - Ryan')
    path = os.path.join('C:\\Dev\\Nova\\Nova')
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

from datareporting.models import *
from django.contrib.auth.models import User

def run_algo():

    for task in ManualTaskQueue.objects.all().filter(task_queued=1, task_running=0):
        report = task.report_name
        try:
            report.error_status = None
            report.save()
            task.task_running = 1
            task.save()
            parameter = task.report_name.series_parameter
            if parameter is None:
                parameter = 0

            #meps_comp_entries:
            if task.report_name.report_name == 'meps_comp_entries':
                #Get datalake data
                with pyodbc.connect("DSN=hive.ucles.internal", autocommit=True) as conn:
                    df = pd.read_sql(f'''
                        select distinct
                            centre_id as centre_id,
                            sap_centre_id as sap_centre_id,
                            c4c_centre_id as c4c_centre_id,
                            centre_name as centre_name,
                            cno_postcode as cno_postcode,
                            cno_country as cno_country,
                            cand_uniq_id as cand_uniq_id,
                            school_or_private as school_or_private,
                            cand_ses_id as cand_ses_id,
                            ses_sid as ses_sid,
                            ses_name as ses_name,
                            ses_month as ses_month,
                            ses_year as ses_year,
                            financial_year as financial_year,
                            qualif as qualif,
                            ass_code as ass_code,
                            ass_ver_no as ass_ver_no,
                            opt_code as opt_code,
                            comp_list as comp_list,
                            comp_id as comp_id,
                            kpi_entries_comp as kpi_entries_comp,
                            qua_name_sh as qua_name_sh,
                            ass_name_sh as ass_name_sh,
                            opt_name as opt_name,
                            retake_ind as retake_ind,
                            exam_start_date as exam_start_date,
                            exam_time_of_day as exam_time_of_day,
                            datetime_received as datetime_received,
                            create_datetime as create_datetime,
                            mod_timestamp as mod_timestamp,
                            sid as sid,
                            name as name,
                            sex_code as sex_code,
                            date_of_birth as date_of_birth,
                            national_id as national_id
                        from cie.meps_comp_entries
                        where ses_sid in ({parameter}) 
                                            ''', conn)

                meps_comp_entries.objects.all().delete()

                def insert_to_model(row):
                    meps_comp_entries.objects.create(
                        centre_id = row['centre_id'],
                        sap_centre_id = row['sap_centre_id'],
                        c4c_centre_id = row['c4c_centre_id'],
                        centre_name = row['centre_name'],
                        cno_postcode = row['cno_postcode'],
                        cno_country = row['cno_country'],
                        cand_uniq_id = row['cand_uniq_id'],
                        school_or_private = row['school_or_private'],
                        cand_ses_id = row['cand_ses_id'],
                        ses_sid = row['ses_sid'],
                        ses_name = row['ses_name'],
                        ses_month = row['ses_month'],
                        ses_year = row['ses_year'],
                        financial_year = row['financial_year'],
                        qualif = row['qualif'],
                        ass_code = row['ass_code'],
                        ass_ver_no = row['ass_ver_no'],
                        opt_code = row['opt_code'],
                        comp_list = row['comp_list'],
                        comp_id = row['comp_id'],
                        kpi_entries_comp = row['kpi_entries_comp'],
                        qua_name_sh = row['qua_name_sh'],
                        ass_name_sh = row['ass_name_sh'],
                        opt_name = row['opt_name'],
                        retake_ind = row['retake_ind'],
                        exam_start_date = row['exam_start_date'],
                        exam_time_of_day = row['exam_time_of_day'],
                        datetime_received = row['datetime_received'],
                        create_datetime = row['create_datetime'],
                        mod_timestamp = row['mod_timestamp'],
                        sid = row['sid'],
                        name = row['name'],
                        sex_code = row['sex_code'],
                        date_of_birth = row['date_of_birth'],
                        national_id = row['national_id'],
                )

            #cie_ciedirect_enquiry:
            if task.report_name.report_name == 'ciedirect_enquiry':
                #Get datalake data
                with pyodbc.connect("DSN=hive.ucles.internal", autocommit=True) as conn:
                    df = pd.read_sql(f'''
                        select 
                        sessid as sessid,
                        enquiryid as enquiryid,
                        epsenquiryid as epsenquiryid
                        from cie.ciedirect_enquiry
                        where sessid in ({parameter}) 
                                            ''', conn)
                
                ciedirect_enquiry.objects.all().delete()

                def insert_to_model(row):
                    ciedirect_enquiry.objects.create(
                        sessid = row['sessid'],
                        enquiryid = row['enquiryid'],
                        epsenquiryid = row['epsenquiryid'],
                    )

            #ciedirect_enquirystatus:
            if task.report_name.report_name == 'ciedirect_enquirystatus':
                #Get datalake data
                with pyodbc.connect("DSN=hive.ucles.internal", autocommit=True) as conn:
                    df = pd.read_sql(f'''
                        select 
                        enquiryid as enquiryid,
                        
                        enquirystatus as enquirystatus,
                        cast(datetime as date) as datetime
                        from cie.ciedirect_enquirystatus
                        where partition_year in ({parameter}) 
                                            ''', conn)
                
                ciedirect_enquirystatus.objects.all().delete()

                def insert_to_model(row):
                    ciedirect_enquirystatus.objects.create(
                        enquiryid = row['enquiryid'],
                        enquirystatus = row['enquirystatus'],
                        datetime = row['datetime'],
                    )

             #centre_enquiry_requests:
            if task.report_name.report_name == 'centre_enquiry_requests':
                #Get datalake data
                with pyodbc.connect("DSN=hive.ucles.internal", autocommit=True) as conn:
                    df = pd.read_sql(f'''
                        select
                        sid as sid,
                        ses_sid as ses_sid,
                        cnu_id as cnu_id,
                        status as status,
                        cast(created_datetime as date) as created_datetime,
                        cast(completed_datetime as date) as completed_datetime

                        from ar_meps_req_prd.centre_enquiry_requests

                        where ses_sid IN ({parameter}) 
                                            ''', conn)
                
                centre_enquiry_requests.objects.all().delete()

                def insert_to_model(row):
                    centre_enquiry_requests.objects.create(
                        sid = row['sid'],
                        ses_sid = row['ses_sid'],
                        cnu_id = row['cnu_id'],
                        status = row['status'],
                        created_datetime = row['created_datetime'],
                        completed_datetime = row['completed_datetime'],
                    )

             #enquiry_request_parts:
            if task.report_name.report_name == 'enquiry_request_parts':
                #Get datalake data
                with pyodbc.connect("DSN=hive.ucles.internal", autocommit=True) as conn:
                    df = pd.read_sql(f'''
                        select 
                        sid as sid,
                        cer_sid as cer_sid,
                        es_service_code as es_service_code,
                        booked_in_error_ind as booked_in_error_ind

                        from ar_meps_req_prd.enquiry_request_parts

                        where year(load_date) >= {parameter}
                                            ''', conn)
                
                enquiry_request_parts.objects.all().delete()

                def insert_to_model(row):
                    enquiry_request_parts.objects.create(
                        sid = row['sid'],
                        cer_sid = row['cer_sid'],
                        es_service_code = row['es_service_code'],
                        booked_in_error_ind = row['booked_in_error_ind'],
                    )

             #enquiry_components:
            if task.report_name.report_name == 'enquiry_components':
                #Get datalake data
                with pyodbc.connect("DSN=hive.ucles.internal", autocommit=True) as conn:
                    df = pd.read_sql(f'''
                        select 
                        sid as sid,
                        ccm_ass_code as ccm_ass_code,
                        ccm_asv_ver_no as ccm_asv_ver_no,
                        ccm_com_id as ccm_com_id,
                        erp_sid as erp_sid

                        from ar_meps_req_prd.enquiry_components

                        where ccm_ses_sid IN ({parameter})
                                            ''', conn)
                
                enquiry_components.objects.all().delete()

                def insert_to_model(row):
                    enquiry_components.objects.create(
                        sid = row['sid'],
                        ccm_ass_code = row['ccm_ass_code'],
                        ccm_asv_ver_no = row['ccm_asv_ver_no'],
                        ccm_com_id = row['ccm_com_id'],
                        erp_sid = row['erp_sid']
                    )

             #all_products:
            if task.report_name.report_name == 'all_products':
                #Get datalake data
                with pyodbc.connect("DSN=hive.ucles.internal", autocommit=True) as conn:
                    df = pd.read_sql(f'''
                        select
                        ses_sid as ses_sid,
                        ass_code as ass_code,
                        asv_ver_no as asv_ver_no,
                        com_id as com_id,
                        qua_name as qua_name

                        from ar_sts_sts.all_products

                        where ses_sid IN ({parameter})
                                            ''', conn)
                
                all_products.objects.all().delete()

                def insert_to_model(row):
                    all_products.objects.create(
                        ses_sid = row['ses_sid'],
                        ass_code = row['ass_code'],
                        asv_ver_no = row['asv_ver_no'],
                        com_id = row['com_id'],
                        qua_name = row['qua_name'],
                    )

            df.apply(insert_to_model, axis=1)

            task.task_completion_date = timezone.now()
            report.last_updated = timezone.now()
            Row_Count = len(df)
            report.row_count = Row_Count
            if Row_Count == 0:
                report.error_status = 'No Data In Table'
            else:
                report.error_status = None
            task.task_queued = 0
            task.task_running = 0
            task.save()
            report.save()
        except Exception as e:
            task.task_queued = 0
            task.task_running = 0
            report.error_status = 'SQL Failed To Run'
            report.save()
            task.save()  
            print(e)

            # More tasks can be checked for using IF statement here...



run_algo()

end_time = time.time()
execution_time = end_time - start_time
print("Script execution time:", execution_time, "seconds")