from openpyxl import load_workbook
import sys
import os
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

from enquiries.models import TaskManager, EnquiryPersonnelDetails, ScriptApportionment, EnquiryComponentElements, CentreEnquiryRequests, EnquiryComponents, EnquiryComponentsHistory, TaskTypes, ScaledMarks
from django.contrib.auth.models import User

ec_list = ['2145736',
]

def run_algo():
    for app_task in TaskManager.objects.filter(task_id='NEWMIS', ec_sid__in = ec_list):
        if ScriptApportionment.objects.filter(ec_sid=app_task.ec_sid.ec_sid, apportionment_invalidated=0).exists():
            #task data pullled in here
            task_pk = app_task.pk
            script_id = app_task.ec_sid.ec_sid
            print(script_id)
            task_enquiry_id = app_task.enquiry_id.enquiry_id
            syll_comp = app_task.ec_sid.eps_ass_code + "/" + app_task.ec_sid.eps_com_id
            if EnquiryComponentElements.objects.filter(ec_sid=script_id).exists():
                if EnquiryComponentElements.objects.get(ec_sid=script_id).eb_sid is not None:
                    batch_no = EnquiryComponentElements.objects.get(ec_sid=script_id).eb_sid.eb_sid
                else:
                    print('No batch number')
                    continue
            else:
                print('No batch number')
                continue              
            centre_no = app_task.enquiry_id.centre_id
            cand_no = app_task.ec_sid.erp_sid.eps_cand_id
            cand_name = app_task.ec_sid.erp_sid.stud_name
            original_exm = EnquiryComponentsHistory.objects.get(ec_sid=script_id).exm_position
            #TODO: This is dangerous as it assumes a specific apportionemtn and is part of a wider bug on duplicates
            rev_exm = EnquiryPersonnelDetails.objects.filter(enpe_sid=ScriptApportionment.objects.filter(ec_sid=script_id, apportionment_invalidated=0).first().enpe_sid).first().exm_examiner_no
            #This is all to get the scaled mark
            scale_ass_code = app_task.ec_sid.eps_ass_code
            scale_comp_id = app_task.ec_sid.eps_com_id
            scale_centre_no = app_task.enquiry_id.centre_id
            scale_cand_no = app_task.ec_sid.erp_sid.eps_cand_id
            print(scale_ass_code + " " + scale_comp_id + " " + scale_centre_no + " " + scale_cand_no)
            if ScaledMarks.objects.filter(eps_ass_code=scale_ass_code,eps_com_id=scale_comp_id,eps_cnu_id=scale_centre_no,eps_cand_no=scale_cand_no).exists():
                original_mark = ScaledMarks.objects.filter(eps_ass_code=scale_ass_code,eps_com_id=scale_comp_id,eps_cnu_id=scale_centre_no,eps_cand_no=scale_cand_no).first().scaled_mark
                if original_mark is None:
                    print("No Valid Scaled Mark")
                    continue
                else:
                    original_mark = int(original_mark.split('.')[0])
            else:
                print("No Valid Scaled Mark")
                continue
            cred_no = ScriptApportionment.objects.filter(ec_sid=script_id, apportionment_invalidated=0).first().enpe_sid.per_sid.exm_creditor_no

            workbook = load_workbook(filename="Y:\Operations\Results Team\Enquiries About Results\\0.RPA_MIS Returns\EARTemplate1.xlsx")
            sheet = workbook.active

            #Syll/Comp
            sheet["A2"] = syll_comp
            #Batch
            sheet["I2"] = batch_no
            #Centre
            sheet["A4"] = centre_no
            #Cand no
            sheet["B4"] = cand_no
            #Cand name
            sheet["C4"] = cand_name
            #Orig Exm
            sheet["D4"] = original_exm
            #Rev Exm
            sheet["E4"] = rev_exm
            #Scaled (prev) mark
            sheet["F4"] = original_mark
            workbook.save(filename="Y:\Operations\Results Team\Enquiries About Results\\0.RPA_MIS Returns\Outbound Copies\\Examiner-" + cred_no + "_BATCH_" + batch_no + "_MIS.xlsx")

run_algo()