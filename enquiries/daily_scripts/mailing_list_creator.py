import sys
import os
import django
import datetime

from django.conf import settings
import os

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

from enquiries.models import MailingList, MailingListScripts, TaskManager, EnquiryComponentElements, ScriptApportionment, ExaminerEmailOverride

# TODO: handle errors in a constructive way
all_open_retmis = TaskManager.objects.filter(task_id='RETMIS', task_completion_date__isnull=True) #get all open RETMIS scripts (as object)
all_scripts_to_insert = [] #empty array to place objects in for bulk upload
for retmis in all_open_retmis:
    if not TaskManager.objects.filter(task_id='NRMACC', task_completion_date__isnull=True, ec_sid=retmis.ec_sid.ec_sid).exists(): #if script is hard-copy (NRMACC), do not add to emailing list
        #Create a mailing list item, if none exists, by checking SciprtApportionment table
        creditor_no_obj = ScriptApportionment.objects.filter(apportionment_invalidated=0,script_marked=1,ec_sid=retmis.ec_sid.ec_sid).first().enpe_sid.per_sid #Get creditor number for this script
        #check for overidden email address
        if ExaminerEmailOverride.objects.filter(creditor=creditor_no_obj).exists():
            email_address = ExaminerEmailOverride.objects.filter(creditor=creditor_no_obj).first().examiner_email_manual
            email_or = 1
        else:
            email_address = creditor_no_obj.exm_email
            email_or = 0
        print(email_address)
        if MailingList.objects.filter(exm_creditor_no=creditor_no_obj.exm_creditor_no,send_date=datetime.date.today()).exists():
            #check if mailing item already exists, and update it
            mailing_list_obj = MailingList.objects.get(exm_creditor_no=creditor_no_obj.exm_creditor_no,send_date=datetime.date.today())
            if email_or == 1:
                mailing_list_obj.email_address = email_address
                mailing_list_obj.save()
        else: 
            #create the mailing list item in the DB
            mailing_list_obj = MailingList.objects.create(
                exm_creditor_no_id = creditor_no_obj.exm_creditor_no,
                email_address = email_address,
                email_name = creditor_no_obj.exm_title + " " + creditor_no_obj.exm_forename + " " + creditor_no_obj.exm_initials + " " + creditor_no_obj.exm_surname,
                send_date = datetime.date.today(),
            )


        #calculate SLA depending on if Singapore or Priority
        if retmis.ec_sid.erp_sid.cer_sid.ministry_flag == "S" or "P" in retmis.ec_sid.erp_sid.service_code:
            sla_days = 2
        else:
            sla_days = 5
        #manage due date several days after task creatiuon date
        due_date = retmis.task_creation_date + datetime.timedelta(sla_days)

        #prepare queryset object for insertion
        #TODO: Explain _id_id as reverse to FK
        all_scripts_to_insert.append(
            MailingListScripts(
                mailing_list = mailing_list_obj,
                ec_sid_id = retmis.ec_sid.ec_sid,
                eb_sid_id = EnquiryComponentElements.objects.filter(ec_sid=retmis.ec_sid.ec_sid).first().eb_sid.eb_sid,
                due_date = due_date,
                service_code = retmis.ec_sid.erp_sid.service_code,
                syll_comp = retmis.ec_sid.eps_ass_code + "/" + retmis.ec_sid.eps_com_id,
                centre_id = retmis.ec_sid.erp_sid.eps_centre_id,
                candidate_id = retmis.ec_sid.erp_sid.eps_cand_id
            )
        )

    #remove old data if it is for the same day, bulk insert new data
    MailingListScripts.objects.filter(mailing_list__send_date=datetime.date.today()).delete()
    MailingListScripts.objects.bulk_create(all_scripts_to_insert)