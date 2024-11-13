import sys
import os
import django
from django.utils import timezone
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
    print('UAT - Check')
    path = os.path.join('C:\\Dev\\nova')
    sys.path.append(path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings'

django.setup()

from pdq.models import PDQSessions, PDQEntries
from django.contrib.auth.models import User

def run_algo():
    sessions = PDQSessions.objects.filter(visible_session=1)
    for session in sessions:
        session_id = session.session_id
        # # Get datalake data - Centre Enquiry Requests
        with pyodbc.connect("DSN=hive.ucles.internal", autocommit=True) as conn:
            df = pd.read_sql(f'''
                select 
                d.ses_sid as session_id,
                d.centre_id as centre_number,
                d.cand_ses_id as candidate_id,
                d.ass_code as syllabus_code,
                d.comp_id as component_id,
                a.currentgrade as syllabus_grade
                from cie.meps_comp_entries d
                left join cie.ods_candidateoptionresults a
                on cast(a.candidatenumber as string) = d.cand_ses_id
                and a.assessmentcode = d.ass_code 
                and cast(a.sessionid as string) = d.ses_sid 
                and a.centrenumber = d.centre_id
                and a.candidatenumber = d.cand_ses_id
                where d.ses_sid in ({session_id});
                                    ''', conn)
               
        def insert_to_model_pdqentries(row):
            if PDQEntries.objects.filter(session_id = row['session_id'],centre_number = row['centre_number'],candidate_id = row['candidate_id'],syllabus_code = row['syllabus_code'],component_id = row['component_id']).exists():
                PDQEntries.objects.filter(session_id = row['session_id'],centre_number = row['centre_number'],candidate_id = row['candidate_id'],syllabus_code = row['syllabus_code'],component_id = row['component_id']).update(
                    session_id = PDQSessions.objects.get(session_id=row['session_id']),
                    centre_number = row['centre_number'],
                    candidate_id = row['candidate_id'],
                    syllabus_code = row['syllabus_code'],
                    component_id = row['component_id'],
                    syllabus_grade = row['syllabus_grade'],
                )
            else:
                PDQEntries.objects.create(
                    session_id = PDQSessions.objects.get(session_id=row['session_id']),
                    centre_number = row['centre_number'],
                    candidate_id = row['candidate_id'],
                    syllabus_code = row['syllabus_code'],
                    component_id = row['component_id'],
                    syllabus_grade = row['syllabus_grade'],
                )

        df.apply(insert_to_model_pdqentries, axis=1)
        print("PDQ Entries loaded:" + str(datetime.datetime.now()))

run_algo()