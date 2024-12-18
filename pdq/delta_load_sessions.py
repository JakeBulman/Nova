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

from pdq.models import AllSessions
from django.contrib.auth.models import User


def run_algo():

    # # Get datalake data - Centre Enquiry Requests
    with pyodbc.connect("DSN=hive.ucles.internal", autocommit=True) as conn:
        df = pd.read_sql(f'''
                        select 
                        a.sid as session_id, 
                        a.name as session_name, 
                        a.year as session_year, 
                        a.sty_seq_no as session_sequence 
                        from cie.meps_all_sessions a
                        where a.year > YEAR(CURRENT_DATE())-2 and a.start_date is not null and a.sty_id <> 'IELTS'
                                ''', conn)
    
    def insert_to_model_allsessions(row):
        if AllSessions.objects.filter(session_id = row['session_id']).exists():
            AllSessions.objects.filter(session_id = row['session_id']).update(
                session_id = row['session_id'],
                session_name = row['session_name'],
                session_year = row['session_year'],
                session_sequence = row['session_sequence'],

            )
        else:
            AllSessions.objects.create(
                session_id = row['session_id'],
                session_name = row['session_name'],
                session_year = row['session_year'],
                session_sequence = row['session_sequence'],
            )

    df.apply(insert_to_model_allsessions, axis=1)
    print("AllSessions loaded:" + str(datetime.datetime.now()))

run_algo()