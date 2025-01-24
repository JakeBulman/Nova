from openpyxl import load_workbook
import sys
import os
import shutil
import django
from django.utils import timezone
import win32com.client as win32

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

from enquiries.models import TaskManager, EnquiryComponents, CentreEnquiryRequests, EnquiryBatches, EnquiryComponentElements, MisReturnData, ScriptApportionment, EnquiryPersonnelDetails, TaskTypes, EarServerSettings

def run_algo():
    import os
    sessions = str(EarServerSettings.objects.get(pk=1).session_id_list).split(',')
    for file in os.listdir("\\\\filestorage\cie\Operations\Results Team\Enquiries About Results\\" + mis_folder + "\Inbound\\"):
        filename=os.path.join("\\\\filestorage\cie\Operations\Results Team\Enquiries About Results\\" + mis_folder + "\Inbound\\", file)
        new_filename=os.path.join("\\\\filestorage\cie\Operations\Results Team\Enquiries About Results\\" + mis_folder + "\Inbound\COMPLETE\\", file)
        error_filename=os.path.join("\\\\filestorage\cie\Operations\Results Team\Enquiries About Results\\" + mis_folder + "\Inbound\FILE_CHECKS\\", file)
        copy_filename=os.path.join("\\\\filestorage\cie\Operations\Results Team\Enquiries About Results\\" + mis_folder + "\Inbound\COPY\\", file)
        if file.endswith(".xlsx") or file.endswith(".XLSX") or file.endswith(".xls"):
            try:
                workbook = load_workbook(filename)
                shutil.copy(filename, copy_filename)
            except:
                print("Bad file type: " + file)
                #Move file to error folder
                shutil.move(filename, error_filename)
                continue
            try:
                sheet = workbook['MIS & Justifications']
            except:
                print("No Sheet Found")
                #Move file to error folder
                shutil.move(filename, error_filename)
                continue

            eb_sid = sheet["I2"].value
            ec_sid = None
            if EnquiryComponentElements.objects.filter(eb_sid=eb_sid).exists():
                ec_sid = EnquiryComponentElements.objects.filter(eb_sid=eb_sid).first().ec_sid.ec_sid
                task_enquiry_id = EnquiryComponentElements.objects.filter(eb_sid=eb_sid).first().ec_sid.erp_sid.cer_sid.enquiry_id

            task_pk = None
            try:
                #expected_exm = EnquiryPersonnelDetails.objects.filter(enpe_sid=ScriptApportionment.objects.get(ec_sid=ec_sid, apportionment_invalidated=0).enpe_sid).first()
                expected_exm = EnquiryPersonnelDetails.objects.filter(enpe_sid=ScriptApportionment.objects.get(ec_sid=ec_sid, apportionment_invalidated=0).enpe_sid,session__in=sessions).first()
                if TaskManager.objects.filter(task_id='RETMIS', ec_sid=ec_sid ,task_completion_date__isnull=True).exists():
                    task_pk = TaskManager.objects.filter(task_id='RETMIS', ec_sid=ec_sid ,task_completion_date__isnull=True).first().pk
                if task_pk is not None and str(expected_exm.exm_examiner_no).strip()==str(sheet["E4"].value).strip():
                    if MisReturnData.objects.filter(ec_sid=ec_sid).exists():
                        MisReturnData.objects.filter(ec_sid=ec_sid).update(
                            eb_sid = EnquiryBatches.objects.get(eb_sid=eb_sid),
                            ec_sid = EnquiryComponents.objects.get(ec_sid=ec_sid),
                            original_exm = str(sheet["D4"].value).strip(),
                            rev_exm = str(sheet["E4"].value).strip(),
                            original_mark = str(sheet["F4"].value).strip(),
                            mark_status = str(sheet["G4"].value).strip(),
                            revised_mark = str(sheet["H4"].value).strip(),
                            justification_code = str(sheet["I4"].value).strip(),
                            remark_reason = str(sheet["B40"].value).strip(),
                            remark_concern_reason = str(sheet["B50"].value).strip()
                        )
                    else:
                        MisReturnData.objects.create(
                            eb_sid = EnquiryBatches.objects.get(eb_sid=eb_sid),
                            ec_sid = EnquiryComponents.objects.get(ec_sid=ec_sid),
                            original_exm = str(sheet["D4"].value).strip(),
                            rev_exm = str(sheet["E4"].value).strip(),
                            original_mark = str(sheet["F4"].value).strip(),
                            mark_status = str(sheet["G4"].value).strip(),
                            revised_mark = str(sheet["H4"].value).strip(),
                            justification_code = str(sheet["I4"].value).strip(),
                            remark_reason = str(sheet["B40"].value).strip(),
                            remark_concern_reason = str(sheet["B50"].value).strip()
                        )

                    #Move file to completed folder
                    shutil.move(filename, new_filename)

                    #Create next step in chain (MISVRM), now split if SEAB to allow TL pickup
                    if CentreEnquiryRequests.objects.get(enquiry_id=task_enquiry_id).ministry_flag == 'S':
                        TaskManager.objects.create(
                            enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task_enquiry_id),
                            ec_sid = EnquiryComponents.objects.get(ec_sid=ec_sid),
                            task_id = TaskTypes.objects.get(task_id = 'MISVRF'),
                            task_assigned_to = None,
                            task_assigned_date = None,
                            task_completion_date = None
                        )
                        mis_data = MisReturnData.objects.filter(ec_sid=ec_sid).first()
                        mis_data.error_status = "SEAB Component"
                        mis_data.save()
                    else:
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
                    #Move file to error folder
                    shutil.move(filename, error_filename)

            except:
                pass


run_algo()