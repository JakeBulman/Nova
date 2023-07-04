import sys
import os
import django
from django.utils import timezone
import datetime


sys.path.append('C:/Dev/redepplan')
os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings'
django.setup()
from enquiries.models import TaskManager, EnquiryComponents, CentreEnquiryRequests, ScriptApportionmentExtension
from django.contrib.auth.models import User

def run_algo():
    for task in TaskManager.objects.filter(task_id='GDWAIT', task_completion_date__isnull=False):

        app_complete_check = False
        #check if completed apportion task is available
        enquiry_id = task.enquiry_id.enquiry_id
        comp_list_newmis = []
        for comp in TaskManager.objects.filter(task_id='NEWMIS', enquiry_id=enquiry_id):
            comp_list_newmis.append(comp.ec_sid.ec_sid)
        comp_list_gdwait = []
        for comp in TaskManager.objects.filter(task_id='GDWAIT', enquiry_id=enquiry_id, task_completion_date__isnull=False):
            comp_list_gdwait.append(comp.ec_sid.ec_sid)

        comp_list_newmis.sort()
        comp_list_gdwait.sort()

        app_complete_check = comp_list_newmis == comp_list_gdwait
        
        if app_complete_check:
            TaskManager.objects.create(
                enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
                ec_sid = None,
                task_id = 'GRDREL',
                task_assigned_to = User.objects.get(id=33),
                task_assigned_date = timezone.now(),
                task_completion_date = None
            )
                
            TaskManager.objects.filter(pk=task.pk,task_id='GDWAIT').update(task_completion_date=timezone.now())   

run_algo()