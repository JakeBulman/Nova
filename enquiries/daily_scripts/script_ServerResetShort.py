import sys
import os
import django
import datetime


print('DEV')
path = os.path.join('C:\\Users\\bulmaj\\OneDrive - Cambridge\\Desktop\\Dev\\Nova')
sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings_dev'

django.setup()

from enquiries.models import CentreEnquiryRequests, TaskManager, ScriptApportionment, EnquiryComponentsPreviousExaminers, MisReturnData, ScriptApportionmentExtension, EsmcsvDownloads, TaskTypes

def clear_tables():
    TaskManager.objects.all().delete()
    ScriptApportionment.objects.all().delete()
    EnquiryComponentsPreviousExaminers.objects.all().delete()
    MisReturnData.objects.all().delete()
    ScriptApportionmentExtension.objects.all().delete()
    EsmcsvDownloads.objects.all().delete()

    print('Tables Cleared')

def load_core_tables():

    start_time = datetime.datetime.now()
    print("Start Time:" + str(datetime.datetime.now()))

    service_list = ['1','1S','2','2P','2PS','2S','ASC','ASR','3']
    to_insert = []
    for enquiry in CentreEnquiryRequests.objects.exclude(enquiry_tasks__task_id='INITCH').filter(enquiries__service_code__in=service_list):
        enquiry_id = enquiry.enquiry_id
        enquiry_obj = enquiry
        to_insert.append(
            TaskManager(
                enquiry_id = enquiry_obj,
                ec_sid = None,
                task_id_id = 'INITCH',
                task_assigned_to = None,
                task_assigned_date = None,
                task_completion_date = None
            )
        )
    TaskManager.objects.bulk_create(to_insert)
    print("IEC loaded:" + str(datetime.datetime.now()))


    end_time = datetime.datetime.now()
    print(end_time - start_time)

clear_tables()
load_core_tables()
