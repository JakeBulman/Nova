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

from enquiries.models import CentreEnquiryRequests, EnquiryRequestParts, EnquiryComponents, EnquiryPersonnel, EnquiryPersonnelDetails, EnquiryBatches, EnquiryComponentElements, TaskManager, UniqueCreditor, ScriptApportionment, EnquiryComponentsHistory, EnquiryComponentsExaminerChecks, EnquiryComponentsPreviousExaminers, MisReturnData, ScriptApportionmentExtension, EsmcsvDownloads, EarServerSettings, TaskTypes, EnquiryGrades, EnquiryDeadline, ExaminerPanels, MarkTolerances, ScaledMarks

def clear_tables():
    CentreEnquiryRequests.objects.all().delete()
    #Cascades to EnquiryRequestParts, EnquiryComponents, EnquiryComponentElements

    TaskManager.objects.all().delete()

    EnquiryBatches.objects.all().delete()

    ExaminerPanels.objects.all().delete()
    UniqueCreditor.objects.all().delete()
    #Cascades to EnquiryPersonnel, EnquiryPersonnelDetails

    TaskManager.objects.all().delete()
    ScriptApportionment.objects.all().delete()
    EnquiryComponentsHistory.objects.all().delete()
    EnquiryComponentsExaminerChecks.objects.all().delete()
    EnquiryComponentsPreviousExaminers.objects.all().delete()
    MisReturnData.objects.all().delete()
    ScriptApportionmentExtension.objects.all().delete()
    EsmcsvDownloads.objects.all().delete()
    MarkTolerances.objects.all().delete()

    print('Tables Cleared')


clear_tables()
