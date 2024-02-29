import sys
import os
import django
from django.utils import timezone
import datetime
from openpyxl import load_workbook
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
    print('UAT - Check')
    path = os.path.join('C:\\Dev\\nova')
    sys.path.append(path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings'

django.setup()

from datareporting.models import Reports, ManualTaskQueue, meps_comp_entries
from django.contrib.auth.models import User

def run_algo():

    for task in ManualTaskQueue.objects.all().filter(task_queued=1, task_running=0):
        task.task_running = 1
        task.save()
        if task.report_name.report_name == 'meps_comp_entries':

            #Limits enquiries to session or enquiry list
            # session_id = models.EarServerSettings.objects.first().session_id_list
            # enquiry_id_list = EarServerSettings.objects.first().enquiry_id_list
            # if enquiry_id_list != '':
            #     enquiry_id_list = ' and sid in (' + enquiry_id_list + ')'
            # print("ENQ:" + enquiry_id_list)

            # # Get datalake data - Enquiry Batches
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
                    where ses_sid in (19818) 
                                 and 
                                        ''', conn) #hardcoded session ID = bad
                
                #where ses_sid in ({session_id}) 

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

            df.apply(insert_to_model, axis=1)

        task.task_completion_date = timezone.now()
        task.report_name.last_updated = timezone.now()
        task.task_queued = 0
        task.task_running = 0
        task.save()

        # More tasks can be checked for using IF statement here...

run_algo()
