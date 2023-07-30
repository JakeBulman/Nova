import sys
import os
import django
import datetime

if os.getenv('DJANGO_DEVELOPMENT') == 'true':
    path = os.path.join('C:\\Users\\bulmaj\\OneDrive - Cambridge\\Desktop\\Dev\\Nova')
    sys.path.append(path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings_dev'
else:
    sys.path.append('C:/Dev/redepplan')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings'

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

    #TODO: Set up initch for each CER
    def insert_to_model():
        queryset = CentreEnquiryRequests.objects.all()
        for e in queryset:        
            TaskManager.objects.create(
                enquiry_id = CentreEnquiryRequests.objects.only('enquiry_id').get(enquiry_id=e.enquiry_id),
                ec_sid = None,
                task_id = TaskTypes.objects.get(task_id = 'INITCH'),
                task_assigned_to = None,
                task_assigned_date = None,
                task_completion_date = None
            )

    insert_to_model()

    end_time = datetime.datetime.now()
    print(end_time - start_time)

