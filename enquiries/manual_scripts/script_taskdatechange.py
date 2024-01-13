from openpyxl import load_workbook
import sys
import os
import django
from django.utils import timezone
import datetime

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

from enquiries.models import TaskManager, RpaFailureAudit, ScriptApportionment, EnquiryComponentElements, CentreEnquiryRequests, EnquiryComponents, EnquiryComponentsHistory, TaskTypes, ScaledMarks,GradeFailureAudit
from django.contrib.auth.models import User

ec_list = [
'2035758',
'2035756',
'2035734',
'2035730',
'2035720',
'2035714',
'2035696',
'2035694',
'2035574',
'2035572',
'2035570',
'2035564',
'2035562',
'2035978',
'2035976',
'2035974',
'2036060',
'2036058',
'2036048',
'2036046',
'2036040',
'2036036',
'2036038',
'2036032',
'2036024',
'2036022',
'2036018',
'2036014',
'2036012',
'2036010',
'2036008',
'2036004',
'2036006',
'2036002',
'2035998',
'2036000',
'2035986',
'2035992',
'2035990',
'2035994',
'2035996',
'2035984',
'2035980',
'2035982',
'2035970',
'2035964',
'2035966',
'2035958',
'2035956',
'2035952',
'2035942',
'2035940',
'2035938',
'2035936',
'2035928',
'2035930',
'2035932',
'2035934',
'2035926',
'2035924',
'2035922',
'2035916',
'2035920',
'2035918',
'2035912',
'2035910',
'2035908',
'2035906',
'2035904',
'2035900',
'2035898',
'2035896',
'2035890',
'2035884',
'2035882',
'2035878',
'2035876',
'2035866',
'2035874',
'2035872',
'2035870',
'2035868',
'2035856',
'2035864',
'2035846',
'2035850',
'2035848',
'2035862',
'2035860',
'2035858',
'2035854',
'2035840',
'2035852',
'2035832',
'2035842',
'2035830',
'2035844',
'2035824',
'2035834',
'2035822',
'2035816',
'2035820',
'2035812',
'2035774',
'2035810',
'2035808',
'2035772',
'2035798',
'2035806',
'2035778',
'2035804',
'2035776',
'2035782',
'2035780',
'2035770',
'2035768',
'2035764',
'2035750',
'2035586',
'2035668',
'2035554',
'2035662',
'2035580',


]

def run_algo():
    for app_task in TaskManager.objects.filter(task_id='RETMIS', ec_sid__in = ec_list):

        new_creation_date = app_task.task_creation_date + datetime.timedelta(1)
        new_assigned_date = app_task.task_assigned_date + datetime.timedelta(1)

        app_task.task_creation_date = new_creation_date
        app_task.task_assigned_date = new_assigned_date

        app_task.save()


run_algo()