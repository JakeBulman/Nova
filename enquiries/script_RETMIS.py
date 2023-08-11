from openpyxl import load_workbook
import sys
import os
import shutil
import django
from django.utils import timezone
import win32com.client as win32

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
    print('UAT')
    sys.path.append('C:/Dev/redepplan')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings'

django.setup()

from enquiries.models import TaskManager, EnquiryComponents, CentreEnquiryRequests, EnquiryBatches, EnquiryComponentElements, MisReturnData, ScriptApportionment, EnquiryPersonnelDetails, TaskTypes

def run_algo():
    import os
    for file in os.listdir("Y:\Operations\Results Team\Enquiries About Results\\0.RPA_MIS Returns\Inbound\\"):
        filename=os.path.join("Y:\Operations\Results Team\Enquiries About Results\\0.RPA_MIS Returns\Inbound\\", file)
        new_filename=os.path.join("Y:\Operations\Results Team\Enquiries About Results\\0.RPA_MIS Returns\Inbound\COMPLETE\\", file)
        error_filename=os.path.join("Y:\Operations\Results Team\Enquiries About Results\\0.RPA_MIS Returns\Inbound\FILE_CHECKS\\", file)
        if file.endswith(".xlsx"):
            workbook = load_workbook(filename)
            sheet = workbook.active

            eb_sid = sheet["I2"].value
            ec_sid = None
            if EnquiryComponentElements.objects.filter(eb_sid=eb_sid).exists():
                ec_sid = EnquiryComponentElements.objects.filter(eb_sid=eb_sid).first().ec_sid.ec_sid
                task_enquiry_id = EnquiryComponentElements.objects.filter(eb_sid=eb_sid).first().ec_sid.erp_sid.cer_sid.enquiry_id

            #TODO add safety checks on file content (or lock down file)
            task_pk = None
            print(ec_sid)
            try:
                expected_exm = EnquiryPersonnelDetails.objects.filter(enpe_sid=ScriptApportionment.objects.get(ec_sid=ec_sid, apportionment_invalidated=0).enpe_sid).first()
                if TaskManager.objects.filter(task_id='RETMIS', ec_sid=ec_sid ,task_completion_date__isnull=True).exists():
                    task_pk = TaskManager.objects.get(task_id='RETMIS', ec_sid=ec_sid ,task_completion_date__isnull=True).pk
                if task_pk is not None and expected_exm.exm_examiner_no==sheet["E4"].value:
                    if MisReturnData.objects.filter(ec_sid=ec_sid).exists():
                        MisReturnData.objects.update(
                            eb_sid = EnquiryBatches.objects.get(eb_sid=eb_sid),
                            ec_sid = EnquiryComponents.objects.get(ec_sid=ec_sid),
                            original_exm = sheet["D4"].value,
                            rev_exm = sheet["E4"].value,
                            original_mark = sheet["F4"].value,
                            mark_status = sheet["G4"].value,
                            revised_mark = sheet["H4"].value,
                            justification_code = sheet["I4"].value,
                            remark_reason = sheet["B40"].value,
                            remark_concern_reason = sheet["B50"].value
                        )
                    else:
                        MisReturnData.objects.create(
                            eb_sid = EnquiryBatches.objects.get(eb_sid=eb_sid),
                            ec_sid = EnquiryComponents.objects.get(ec_sid=ec_sid),
                            original_exm = sheet["D4"].value,
                            rev_exm = sheet["E4"].value,
                            original_mark = sheet["F4"].value,
                            mark_status = sheet["G4"].value,
                            revised_mark = sheet["H4"].value,
                            justification_code = sheet["I4"].value,
                            remark_reason = sheet["B40"].value,
                            remark_concern_reason = sheet["B50"].value
                        )

                        #Move file to completed folder
                        shutil.move(filename, new_filename)

                        #Create next step in chain (MISVRM)
                        TaskManager.objects.create(
                            enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task_enquiry_id),
                            ec_sid = EnquiryComponents.objects.get(ec_sid=ec_sid),
                            task_id = TaskTypes.objects.get(task_id = 'MISVRM'),
                            task_assigned_to = None,
                            task_assigned_date = None,
                            task_completion_date = None
                        )
                        #complete the task
                        TaskManager.objects.filter(pk=task_pk,task_id='RETMIS').update(task_completion_date=timezone.now())
                        ScriptApportionment.objects.filter(ec_sid=ec_sid).update(script_marked=0)

            except:
                pass


run_algo()