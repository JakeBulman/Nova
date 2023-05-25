from openpyxl import load_workbook
import sys
import os
import django
from django.utils import timezone

sys.path.append('C:/Dev/redepplan')
os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings'
django.setup()
from enquiries.models import TaskManager, EnquiryPersonnelDetails, ScriptApportionment, EnquiryComponentElements, CentreEnquiryRequests, EnquiryComponents

def run_algo():
    for app_task in TaskManager.objects.filter(task_id='NEWMIS', task_completion_date__isnull=True):
        #task data pullled in here
        task_pk = app_task.pk
        script_id = app_task.ec_sid.ec_sid
        task_enquiry_id = app_task.enquiry_id.enquiry_id
        syll_comp = app_task.ec_sid.eps_ass_code + "/" + app_task.ec_sid.eps_com_id
        batch_no = EnquiryComponentElements.objects.get(ec_sid=script_id).eb_sid.eb_sid
        centre_no = app_task.enquiry_id.centre_id
        cand_no = app_task.ec_sid.erp_sid.eps_cand_id
        cand_name = app_task.ec_sid.erp_sid.stud_name
        original_exm = 1 # STILL TODO
        rev_exm = EnquiryPersonnelDetails.objects.filter(enpe_sid=ScriptApportionment.objects.get(ec_sid=script_id).enpe_sid).first().exm_examiner_no
        original_mark = 100 # STILL TODO
        cred_no = ScriptApportionment.objects.get(ec_sid=script_id).enpe_sid.per_sid.exm_creditor_no

        #Work to be done by NEWMIS done here 

        workbook = load_workbook(filename="Y:\Operations\Change Delivery Team\Project Documents\EAR Workflow\EARTemplate1.xlsx")
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

        workbook.save(filename="Y:\Operations\Change Delivery Team\Project Documents\EAR Workflow\MIS Outbound\\" + cred_no + "_BATCH_" + batch_no + "_MIS.xlsx")

        #Create next step in chain (RETMIS)
        TaskManager.objects.create(
            enquiry_id = CentreEnquiryRequests.objects.get(enquiry_id=task_enquiry_id),
            ec_sid = EnquiryComponents.objects.get(ec_sid=script_id),
            task_id = 'RETMIS',
            task_assigned_to = None,
            task_assigned_date = None,
            task_completion_date = None
        )
        #complete the task
        TaskManager.objects.filter(pk=task_pk,task_id='NEWMIS').update(task_completion_date=timezone.now())        

run_algo()