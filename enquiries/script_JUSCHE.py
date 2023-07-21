import sys
import os
import django
from django.utils import timezone
import datetime

if os.getenv('DJANGO_DEVELOPMENT') == 'true':
    path = os.path.join('C:\\Users\\bulmaj\\OneDrive - Cambridge\\Desktop\\Dev\\Nova')
    sys.path.append(path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings_dev'
else:
    sys.path.append('C:/Dev/redepplan')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings'

django.setup()

from enquiries.models import TaskManager, EnquiryComponents, CentreEnquiryRequests, MisReturnData
from django.contrib.auth.models import User

def run_algo():
    for task in TaskManager.objects.filter(task_id='JUSCHE', task_completion_date__isnull=True):

        #TODO: JUSCHE logic goes here
        mis_data = MisReturnData.objects.filter(ec_sid=task.ec_sid.ec_sid).first()
        justification_string = mis_data.final_justification_code
        if justification_string is not None:
            if '4' in justification_string:
                mis_data.selected_justification_code = '4'
                mis_data.keying_required = 'Y'
            elif '2' in justification_string:
                mis_data.selected_justification_code = '2'
                mis_data.keying_required = 'Y'
            elif '3' in justification_string:
                mis_data.selected_justification_code = '3'
                mis_data.keying_required = 'Y'
            elif '1' in justification_string:
                mis_data.selected_justification_code = '1'
                mis_data.keying_required = 'Y'
            elif '5' in justification_string:
                mis_data.selected_justification_code = '5'
                mis_data.keying_required = 'N'
            elif '6' in justification_string:
                mis_data.selected_justification_code = '6'
                mis_data.keying_required = 'Y'
            elif '7' in justification_string:
                mis_data.selected_justification_code = '7'
                mis_data.keying_required = 'N'
            elif '8' in justification_string:
                mis_data.selected_justification_code = '8'
                mis_data.keying_required = 'Y'
            mis_data.save()

        TaskManager.objects.create(
            enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task.enquiry_id.enquiry_id),
            ec_sid = EnquiryComponents.objects.get(ec_sid=task.ec_sid.ec_sid),
            task_id = 'MKWAIT',
            task_assigned_to = User.objects.get(username='NovaServer'),
            task_assigned_date = timezone.now(),
            task_completion_date = None
        )
        TaskManager.objects.filter(pk=task.pk,task_id='JUSCHE').update(task_completion_date=timezone.now())       

run_algo()