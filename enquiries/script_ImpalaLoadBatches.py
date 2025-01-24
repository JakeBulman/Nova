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
    print('UAT')
    path = os.path.join('C:\\Dev\\Nova')
    sys.path.append(path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings'
elif os.getenv('DJANGO_PRODUCTION') == 'true':
    print('PRD')
    path = os.path.join('C:\\Dev\\Nova')
    sys.path.append(path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings_prod'
else:
    print('DEV')
    path = os.path.join('C:\\Users\\bulmaj\\OneDrive - Cambridge\\Desktop\\Dev\\Nova')
    sys.path.append(path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings_dev'

django.setup()

from enquiries.models import CentreEnquiryRequests, EnquiryRequestParts, EnquiryComponents, EnquiryPersonnel, EnquiryPersonnelDetails, EnquiryBatches, EnquiryComponentElements, TaskManager, UniqueCreditor, EnquiryComponentsHistory, EnquiryComponentsExaminerChecks, TaskTypes, EarServerSettings, EnquiryGrades, EnquiryDeadline, ExaminerPanels, MarkTolerances, ScaledMarks, CentreEnquiryRequestsExtra, EnquiryRequestPartsExtra, EnquiryComponentsExtra

def load_core_tables():

    start_time = datetime.datetime.now()
    print("Start Time:" + str(datetime.datetime.now()))
    EarServerSettings.objects.update(delta_load_status='Batches Load Starting, first table loading')

    try:
        #Limits enquiries to session or enquiry list
        session_id = EarServerSettings.objects.first().session_id_list
        enquiry_id_list = EarServerSettings.objects.first().enquiry_id_list
        if enquiry_id_list != '':
            enquiry_id_list = ' and cer.sid in (' + enquiry_id_list + ')'


        # Get datalake data - Batches
        with pyodbc.connect("DSN=Impala DL", autocommit=True) as conn:
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

        rolling_insert = []
        def insert_to_model(row):
            try:
                eper_per_sid = int(row['eper_per_sid'])
            except:
                eper_per_sid = None
            rolling_insert.append(
                EnquiryBatches(
                    eb_sid = int(row['eb_sid']),
                    created_date = row['created_date'],
                    enpe_eper_per_sid = eper_per_sid,
                )
            )

        df.apply(insert_to_model, axis=1)
        EnquiryBatches.objects.bulk_create(rolling_insert,update_conflicts=True,unique_fields=['eb_sid'],
                                                update_fields=['created_date','enpe_eper_per_sid']
                                                )
        
        print("Enquiry Batches loaded:" + str(datetime.datetime.now()))
        EarServerSettings.objects.update(delta_load_status='Batches - Table 1 of 2 loaded, Enquiry Batches')


        #Get datalake data - Enquiry Component Elements
        with pyodbc.connect("DSN=Impala DL", autocommit=True) as conn:
            df = pd.read_sql(f'''
                select distinct
                ece.ec_sid as ec_sid,
                ece.status as ece_status,
                ece.eb_sid as eb_sid,
                ece.clerical_mark as clerical_mark,
                ece.mark_after_enquiry as mark_after_enquiry,
                ece.justification_code as justification_code,
                ece.omr_mark_changed_ind as omr_mark_changed_ind,
                ece.omr_mark_confirmed_ind as omr_mark_confirmed_ind,
                ece.clerical_mark_changed_ind as clerical_mark_changed_ind,
                ece.clerical_mark_confirmed_ind as clerical_mark_confirmed_ind,
                ece.me_id as me_id             
                from  ar_meps_req_prd.enquiry_component_elements ece
                left join ar_meps_req_prd.enquiry_components ec
                on ece.ec_sid = ec.sid
                where ec.ccm_ses_sid in ({session_id}) 
                                    ''', conn)
            
        rolling_insert = []
        def insert_to_model(row):
            try:
                eb = int(row['eb_sid'])
            except:
                eb = None
            try:
                rolling_insert.append(
                    EnquiryComponentElements(
                        ec_sid_id = EnquiryComponents.objects.get(ec_sid = int(row['ec_sid'])).ec_sid,
                        ece_status = row['ece_status'][:20],
                        eb_sid_id = eb,
                        clerical_mark = row['clerical_mark'],
                        mark_after_enquiry = row['mark_after_enquiry'],
                        justification_code = row['justification_code'],
                        omr_mark_changed_ind = row['omr_mark_changed_ind'],
                        omr_mark_confirmed_ind = row['omr_mark_confirmed_ind'],
                        clerical_mark_changed_ind = row['clerical_mark_changed_ind'],
                        clerical_mark_confirmed_ind = row['clerical_mark_confirmed_ind'],
                        me_id = row['me_id'],
                    )
                )
            except:
                pass

        df.apply(insert_to_model, axis=1)
        EnquiryComponentElements.objects.all().delete()
        EnquiryComponentElements.objects.bulk_create(rolling_insert)
        print("ECE loaded:" + str(datetime.datetime.now()))

        if os.getenv('DJANGO_PRODUCTION') == 'true':
            EarServerSettings.objects.update(delta_load_status='Batches Load completed at '+str(datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            email = EmailMessage()
            email["From"] = "results.enquiries@cambridge.org"
            email["To"] = "results.enquiries@cambridge.org, jacob.bulman@cambridge.org,jonathon.east@cambridge.org,ben.herbert@cambridge.org,charlotte.weedon@cambridge.org,morgan.jones@cambridge.org,lab.d@cambridgeassessment.org.uk"
            email["Subject"] = "Batches Data Load- SUCCESS"
            email.set_content("Batches load was successful, batches data updated.", subtype='html')

            sender = "results.enquiries@cambridge.org"
            smtp = smtplib.SMTP("smtp0.ucles.internal", port=25) 
            smtp.sendmail(sender, ["results.enquiries@cambridge.org", "jacob.bulman@cambridge.org","jonathon.east@cambridge.org","ben.herbert@cambridge.org","charlotte.weedon@cambridge.org","morgan.jones@cambridge.org","lab.d@cambridgeassessment.org.uk"], email.as_string())
            smtp.quit()


            end_time = datetime.datetime.now()
            print(end_time - start_time)
    except Exception as e:
        print(traceback.format_exc())
        if os.getenv('DJANGO_PRODUCTION') == 'true':
            EarServerSettings.objects.update(delta_load_status='Batches Load failed at '+str(datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            email = EmailMessage()
            email["From"] = "results.enquiries@cambridge.org"
            email["To"] = "results.enquiries@cambridge.org, jacob.bulman@cambridge.org,jonathon.east@cambridge.org,ben.herbert@cambridge.org,charlotte.weedon@cambridge.org,morgan.jones@cambridge.org,lab.d@cambridgeassessment.org.uk"
            email["Subject"] = "Batches Data Load - ERROR"
            email.set_content(f"Batches load has failed, please contact the system administrator for further details. Error: {e}", subtype='html')

            sender = "results.enquiries@cambridge.org"
            smtp = smtplib.SMTP("smtp0.ucles.internal", port=25) 
            smtp.sendmail(sender, ["results.enquiries@cambridge.org", "jacob.bulman@cambridge.org","jonathon.east@cambridge.org","ben.herbert@cambridge.org","charlotte.weedon@cambridge.org","morgan.jones@cambridge.org","lab.d@cambridgeassessment.org.uk"], email.as_string())
            smtp.quit()
            end_time = datetime.datetime.now()
            print(end_time - start_time)

    end_time = datetime.datetime.now()
    print(end_time - start_time)


load_core_tables()
