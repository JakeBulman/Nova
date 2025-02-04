from openpyxl import load_workbook
import sys
import os
import shutil
import django
from django.utils import timezone

if os.getenv('DJANGO_DEVELOPMENT') == 'true':
    print('UAT')
    path = os.path.join('C:\\Dev\\Nova')
    sys.path.append(path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings'
elif os.getenv('DJANGO_PRODUCTION') == 'true':
    print('PRD')
    path = os.path.join('C:\\Dev\\Nova')
    sys.path.append(path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings_prod'
else:
    print('DEV')
    path = os.path.join('C:\\Users\\bulmaj\\OneDrive - Cambridge\\Desktop\\Dev\\Nova')
    sys.path.append(path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings_dev'

django.setup()

from enquiries.models import TaskManager, EnquiryComponents, CentreEnquiryRequests, EnquiryBatches, EnquiryComponentElements, MisReturnData, ScriptApportionment, EnquiryPersonnelDetails, TaskTypes

def run_algo():

            eb_sid = '1018806'
            print(eb_sid)
            ec_sid = None
            if EnquiryComponentElements.objects.filter(eb_sid=eb_sid).exists():
                ec_sid = EnquiryComponentElements.objects.filter(eb_sid=eb_sid).first().ec_sid.ec_sid
                task_enquiry_id = EnquiryComponentElements.objects.filter(eb_sid=eb_sid).first().ec_sid.erp_sid.cer_sid.enquiry_id

            #TODO add safety checks on file content (or lock down file)
            task_pk = None
            print(ec_sid)
            try:
                expected_exm = EnquiryPersonnelDetails.objects.filter(enpe_sid=ScriptApportionment.objects.get(ec_sid=ec_sid, apportionment_invalidated=0).enpe_sid).first()
                
                if TaskManager.objects.filter(task_id='RETMIS', ec_sid=ec_sid).exists():
                    task_pk = TaskManager.objects.filter(task_id='RETMIS', ec_sid=ec_sid).first().pk
                if task_pk is not None:
                    if MisReturnData.objects.filter(ec_sid=ec_sid).exists():
                        print("Update")
                        MisReturnData.objects.filter(ec_sid=ec_sid).update(
                            eb_sid = EnquiryBatches.objects.get(eb_sid=eb_sid),
                            ec_sid = EnquiryComponents.objects.get(ec_sid=ec_sid),
                            original_exm = '01.01',
                            rev_exm = '01.03',
                            original_mark = '41',
                            mark_status = 'Confirmed',
                            revised_mark = None,
                            justification_code = '',
                            remark_reason = '',
                            remark_concern_reason = '',
                        )
                    else:
                        print("Create")
                        MisReturnData.objects.create(
                            eb_sid = EnquiryBatches.objects.get(eb_sid=eb_sid),
                            ec_sid = EnquiryComponents.objects.get(ec_sid=ec_sid),
                            original_exm = '01.01',
                            rev_exm = '01.03',
                            original_mark = '41',
                            mark_status = 'Confirmed',
                            revised_mark = None,
                            justification_code = '',
                            remark_reason = '',
                            remark_concern_reason = '',
                        )

                    #Create next step in chain (MISVRM)
                    if not TaskManager.objects.filter(task_id='MISVRM', ec_sid=ec_sid).exists():
                        print("MISVRM Made")
                        TaskManager.objects.create(
                            enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task_enquiry_id),
                            ec_sid = EnquiryComponents.objects.get(ec_sid=ec_sid),
                            task_id = TaskTypes.objects.get(task_id = 'MISVRM'),
                            task_assigned_to = None,
                            task_assigned_date = None,
                            task_completion_date = None
                        )
                    #complete the task
                    TaskManager.objects.filter(ec_sid=ec_sid,task_id='RETMIS').update(task_completion_date=timezone.now())
                    ScriptApportionment.objects.filter(ec_sid=ec_sid).update(script_marked=0)

                else:
                    print("Expected:" + expected_exm.exm_examiner_no)

            except:
                pass


run_algo()