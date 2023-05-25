import sys
import os
import django
import datetime
sys.path.append('C:/Dev/redepplan')
os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings'
django.setup()
from enquiries.models import TaskManager, EnquiryComponents, EnquiryPersonnel, EnquiryPersonnelDetails, ScriptApportionment, CentreEnquiryRequests
from django.utils import timezone

# Create your views here.
def run_algo():
    for app_task in TaskManager.objects.filter(task_id='AUTAPP', task_completion_date__isnull=True):
        task_pk = app_task.pk
        script_id = app_task.ec_sid.ec_sid
        task_enquiry_id = app_task.enquiry_id.enquiry_id
        print(script_id)
        script_obj = EnquiryComponents.objects.get(ec_sid=script_id)
        examiner_detail_obj = EnquiryPersonnelDetails.objects.filter(ass_code=script_obj.eps_ass_code,com_id=script_obj.eps_com_id).first()
        print(script_obj.eps_ass_code)
        print(script_obj.eps_com_id)
        print(examiner_detail_obj)
        
        if examiner_detail_obj is not None:
            print(examiner_detail_obj.enpe_sid.enpe_sid)
            examiner_obj = EnquiryPersonnel.objects.get(enpe_sid=examiner_detail_obj.enpe_sid.enpe_sid)
            print("check1" + examiner_obj.enpe_sid)
            ScriptApportionment.objects.create(
                enpe_sid = examiner_obj,
                ec_sid =  script_obj
                #script_marked is default to 0
            )

            TaskManager.objects.create(
                enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task_enquiry_id),
                ec_sid = EnquiryComponents.objects.get(ec_sid=script_id),
                task_id = 'BOTAPP',
                task_assigned_to = None,
                task_assigned_date = None,
                task_completion_date = None
            )
            TaskManager.objects.create(
                enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task_enquiry_id),
                ec_sid = EnquiryComponents.objects.get(ec_sid=script_id),
                task_id = 'NEWMIS',
                task_assigned_to = None,
                task_assigned_date = None,
                task_completion_date = None
            )
            #complete the task
            TaskManager.objects.filter(pk=task_pk,task_id='AUTAPP').update(task_completion_date=timezone.now())        

run_algo()