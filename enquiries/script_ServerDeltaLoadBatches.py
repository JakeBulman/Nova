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
    print('UAT - Check')
    path = os.path.join('C:\\Dev\\nova')
    sys.path.append(path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings'

django.setup()

from enquiries.models import EnquiryComponents, EnquiryBatches, EnquiryComponentElements, EarServerSettings

def load_core_tables():

    start_time = datetime.datetime.now()
    print("Start Time:" + str(datetime.datetime.now()))

    #Limits enquiries to session or enquiry list
    session_id = EarServerSettings.objects.first().session_id_list
    enquiry_id_list = EarServerSettings.objects.first().enquiry_id_list
    if enquiry_id_list != '':
        enquiry_id_list = ' and sid in (' + enquiry_id_list + ')'

    print("ENQ:" + enquiry_id_list)

    # # Get datalake data - Enquiry Batches
    with pyodbc.connect("DSN=hive.ucles.internal", autocommit=True) as conn:
        df = pd.read_sql(f'''
            select distinct
            sb.sid as eb_sid,
            sb.created_date as created_date,
            sb.enpe_eper_per_sid as eper_per_sid
            from ar_meps_req_prd.summary_batches sb
            left join ar_meps_req_prd.enquiry_component_elements ece
            on sb.sid = ece.eb_sid
            left join ar_meps_req_prd.enquiry_components ec
            on ec.sid = ece.ec_sid
            where ec.ccm_ses_sid in ({session_id}) 
                                ''', conn)

    def insert_to_model_eb(row):
        if EnquiryBatches.objects.filter(eb_sid = row['eb_sid']).exists():
            EnquiryBatches.objects.filter(eb_sid = row['eb_sid']).update(
                eb_sid = row['eb_sid'],
                created_date = row['created_date'],
                enpe_eper_per_sid = row['eper_per_sid'],
            )
        else:
            try:
                EnquiryBatches.objects.create(
                    eb_sid = row['eb_sid'],
                    created_date = row['created_date'],
                    enpe_eper_per_sid = row['eper_per_sid'],
                )
            except:
                pass

    df.apply(insert_to_model_eb, axis=1)
    print("EB loaded:" + str(datetime.datetime.now()))

    #Get datalake data - Enquiry Components
    with pyodbc.connect("DSN=hive.ucles.internal", autocommit=True) as conn:
        df = pd.read_sql(f'''
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
            where ec.ccm_ses_sid in ({session_id}) 
                                ''', conn)

    def insert_to_model_ec(row):
        if EnquiryComponentElements.objects.filter(ec_sid=row['ec_sid']).exists():
            EnquiryComponentElements.objects.filter(ec_sid=row['ec_sid']).update(
                ec_sid = EnquiryComponents.objects.only('ec_sid').get(ec_sid=row['ec_sid']),
                ece_status = row['ece_status'],
                eb_sid = EnquiryBatches.objects.only('eb_sid').filter(eb_sid=row['eb_sid']).first(),
                clerical_mark = row['clerical_mark'],
                mark_after_enquiry = row['mark_after_enquiry'],
                justification_code = row['justification_code'],
            )   
        else:
            try:
                EnquiryComponentElements.objects.create(
                    ec_sid = EnquiryComponents.objects.only('ec_sid').get(ec_sid=row['ec_sid']),
                    ece_status = row['ece_status'],
                    eb_sid = EnquiryBatches.objects.only('eb_sid').filter(eb_sid=row['eb_sid']).first(),
                    clerical_mark = row['clerical_mark'],
                    mark_after_enquiry = row['mark_after_enquiry'],
                    justification_code = row['justification_code'],
                )   
            except:
                pass


    df.apply(insert_to_model_ec, axis=1)

    print("ECE loaded:" + str(datetime.datetime.now()))

    end_time = datetime.datetime.now()
    print(end_time - start_time)

load_core_tables()
