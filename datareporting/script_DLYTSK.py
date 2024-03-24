import sys
import os
import django
from openpyxl import load_workbook
import pandas as pd
import time
from django.utils import timezone

start_time = time.time()

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

active_dataset_ids = Report_Datasets.objects.filter(report__active=True).values_list('dataset_id', flat=True).distinct()
active_datasets = Datasets.objects.filter(id__in=active_dataset_ids)

for dataset in active_datasets:
    ManualTaskQueue.objects.create(dataset=dataset)
