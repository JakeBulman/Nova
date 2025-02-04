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
    import os
    for file in os.listdir("Y:\Operations\Results Team\Enquiries About Results\\0.RPA_MIS Returns\Inbound\COMPLETE\\"):
        filename=os.path.join("Y:\Operations\Results Team\Enquiries About Results\\0.RPA_MIS Returns\Inbound\COMPLETE\\", file)
        if file.endswith(".xlsx"):
            workbook = load_workbook(filename)
            try:
                sheet = workbook['MIS & Justifications']
            except:
                print("No Sheet Found")
                continue

            eb_sid = sheet["I2"].value
            print(eb_sid)
            ec_sid = None
            if EnquiryComponentElements.objects.filter(eb_sid=eb_sid).exists():
                ec_sid = EnquiryComponentElements.objects.filter(eb_sid=eb_sid).first().ec_sid.ec_sid
                task_enquiry_id = EnquiryComponentElements.objects.filter(eb_sid=eb_sid).first().ec_sid.erp_sid.cer_sid.enquiry_id

            #TODO add safety checks on file content (or lock down file)
            task_pk = None
            print(ec_sid)
            # try:
            expected_exm = EnquiryPersonnelDetails.objects.filter(enpe_sid=ScriptApportionment.objects.get(ec_sid=ec_sid, apportionment_invalidated=0).enpe_sid).first()

            if  expected_exm.exm_examiner_no==sheet["E4"].value:
                if MisReturnData.objects.filter(ec_sid=ec_sid).exists():
                    print('EXIST')
                    a = 1
                    # MisReturnData.objects.filter(ec_sid=ec_sid).update(
                    #     eb_sid = EnquiryBatches.objects.get(eb_sid=eb_sid),
                    #     ec_sid = EnquiryComponents.objects.get(ec_sid=ec_sid),
                    #     original_exm = sheet["D4"].value,
                    #     rev_exm = sheet["E4"].value,
                    #     original_mark = sheet["F4"].value,
                    #     mark_status = sheet["G4"].value,
                    #     revised_mark = sheet["H4"].value,
                    #     justification_code = sheet["I4"].value,
                    #     remark_reason = sheet["B40"].value,
                    #     remark_concern_reason = sheet["B50"].value
                    # )
                else:
                    print('MAKE')
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


run_algo()