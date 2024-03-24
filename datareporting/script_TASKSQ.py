import sys
import os
import django
from django.utils import timezone
import datetime
from openpyxl import load_workbook
import pyodbc
import pandas as pd
import time
from django.apps import apps
from sqlalchemy import create_engine
import psycopg2 
import io

from django.db.models import Min

if os.getenv('DJANGO_DEVELOPMENT') == 'true':
    print('DEV')
    path = os.path.join('C:\\Users\\bulmaj\\OneDrive - Cambridge\\Desktop\\Dev\\Nova')
    sys.path.append(path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings_dev'
elif os.getenv('DJANGO_DEVELOPMENT_RYAN') == 'true':
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

for task in ManualTaskQueue.objects.all().filter(task_queued=1, task_running=0).order_by('id'):
    dataset = task.dataset
    dataset_name = dataset.dataset_name
    dataset_sql = task.dataset.sql
    parameter_name = dataset.parameter_name
    operator = dataset.operator

    report_parameters = Report_Datasets.objects.filter(dataset_id=dataset.id, report__active = True)
    concatenated_parameters = ', '.join(["'"+str(rp.report_parameter)+"'" for rp in report_parameters])

    try:
        dataset.error_status = None
        dataset.save()
        task.task_running = 1
        task.save()
        
        if concatenated_parameters != '':

            with pyodbc.connect("DSN=hive.ucles.internal", autocommit=True) as conn:
                if operator == '=':
                    df = pd.read_sql(f'''{dataset_sql} where {parameter_name} in ({concatenated_parameters})''', conn)
                    
                elif operator == '>=':
                    min_parameter = report_parameters.aggregate(Min('report_parameter'))
                    min_parameter_value = min_parameter['report_parameter__min']
                    print(min_parameter_value)
                    df = pd.read_sql(f'''{dataset_sql} where {parameter_name} >= {min_parameter_value}''', conn)
            
            engine = create_engine('postgresql+psycopg2://postgres:jman@localhost:5432/myproject')

            # Drop old table and create new empty table
            df.head(0).to_sql(f'datareporting_dataset_{dataset_name}', engine, if_exists='replace',index=False)

            conn = engine.raw_connection()
            cur = conn.cursor()
            output = io.StringIO()
            df.to_csv(output, sep='\t', header=False, index=False)
            output.seek(0)
            contents = output.getvalue()
            cur.copy_from(output, f'datareporting_dataset_{dataset_name}', null="")
            conn.commit()
            cur.close()
            conn.close()

            dataset_size = len(df)

            dataset.row_count= dataset_size
        
        task.task_completion_date = timezone.now()
        dataset.last_updated = timezone.now()
        task.task_queued = 0
        task.task_running = 0
        task.save()
        dataset.save()

    except Exception as e:
        task.task_queued = 0
        task.task_running = 0
        dataset.error_status = 'SQL Failed To Run'
        dataset.save()
        task.save()  
        print(e)

script_info = Script_Info.objects.get(script = 'TASKSQ')
script_info.running = False
script_info.save()