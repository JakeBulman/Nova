from openpyxl import load_workbook
import sys
import os
import shutil
import django
from django.utils import timezone
import win32com.client as win32
import datetime
from string import Template

from django.conf import settings
import csv, os

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

from enquiries.models import TaskManager, ScriptApportionmentExtension, UniqueCreditor, EnquiryBatches, EnquiryComponentElements, MisReturnData, ScriptApportionment, EnquiryPersonnelDetails, TaskTypes
from email.message import EmailMessage
import smtplib

examiner_list = []
for task in TaskManager.objects.filter(task_id='RETMIS', task_completion_date__isnull=True):
    script = task.ec_sid
    print(script.ec_sid)
    examiner = ScriptApportionment.objects.get(ec_sid = script, apportionment_invalidated=0).enpe_sid.per_sid.exm_creditor_no
    if examiner not in examiner_list:
      examiner_list.append(examiner)

file_timestamp = timezone.now().strftime("%m_%d_%Y_%H_%M_%S") + "email.csv"
file_location = os.path.join(settings.MEDIA_ROOT, "downloads", file_timestamp).replace('\\', '/')
print(file_location)	

email_list = []
load_file = os.path.join(settings.MEDIA_ROOT, "downloads", "email.csv").replace('\\', '/')
with open(load_file, 'r') as csvfile:
  spamreader = csv.reader(csvfile)
  for row in spamreader:
    email_list.append(row[0])

print(email_list)
for exm in examiner_list:
    uc = UniqueCreditor.objects.get(exm_creditor_no=exm)
    if uc.exm_email in email_list:
        print('BAD EMAIL:'+ uc.exm_email)
    else:
        
        full_name = uc.exm_title+' '+uc.exm_forename+' '+uc.exm_surname
        table_entry = ''
        print(uc.exm_creditor_no + ' ' + full_name)
        enpe_list = []
        for enpe in EnquiryPersonnelDetails.objects.filter(exm_creditor_no=exm):
            if enpe.enpe_sid.enpe_sid not in enpe_list:
                enpe_list.append(enpe.enpe_sid.enpe_sid)
        for enpe2 in enpe_list:
            for script in ScriptApportionment.objects.filter(enpe_sid=enpe2, apportionment_invalidated=0, script_marked=1):
                print('Script:' + script.ec_sid.ec_sid)
                if not TaskManager.objects.filter(task_id='NRMACC', task_completion_date__isnull=True, ec_sid=script.ec_sid.ec_sid).exists() and TaskManager.objects.filter(task_id='RETMIS', task_completion_date__isnull=True, ec_sid=script.ec_sid.ec_sid).exists():
                    task = TaskManager.objects.filter(task_id='RETMIS', task_completion_date__isnull=True, ec_sid=script.ec_sid.ec_sid).first()
                    extension_total = 0
                    exmsla_count = TaskManager.objects.filter(task_id='EXMSLA', ec_sid=task.ec_sid.ec_sid, task_completion_date__isnull=True).count()
                    for e in ScriptApportionmentExtension.objects.filter(task_id=TaskManager.objects.filter(ec_sid=task.ec_sid,task_id='RETMIS', task_completion_date__isnull=True).first().pk):
                        extension_total = int(e.extension_days) + extension_total
                    due_date = task.task_creation_date + datetime.timedelta(days=5) + datetime.timedelta(days=extension_total)
                    due_date = due_date.strftime('%d/%m/%Y')
                    service = script.ec_sid.erp_sid.service_code
                    batch = EnquiryComponentElements.objects.get(ec_sid=script.ec_sid.ec_sid).eb_sid.eb_sid
                    syll_comp = script.ec_sid.eps_ass_code + '/' + script.ec_sid.eps_com_id
                    centre_id = script.ec_sid.erp_sid.eps_centre_id
                    cand_id = script.ec_sid.erp_sid.eps_cand_id

                    table_entry = table_entry + f"""
                    <tr>
                      <td>{due_date}</td>
                      <td>{service}</td>
                      <td>{batch}</td>
                      <td>{syll_comp}</td>
                      <td>{centre_id}</td>
                      <td>{cand_id}</td>
                    </tr>
                    """    
                    
        HtmlBody = Template("""

        <style>
        #customers {
          font-family: Arial, Helvetica, sans-serif;
          border-collapse: collapse;
          width: 100%;
        }

        #customers td, #customers th {
          border: 1px solid #ddd;
          padding: 8px;
        }

        #customers th {
          padding-top: 12px;
          padding-bottom: 12px;
          text-align: left;
          background-color: #04AA6D;
          color: white;
        }
        </style>

        <body>
        <p>Dear $full_name</p>

        <h3>Enquiry About Results – Review of Marking </h3>

        <p>We have been asked to provide a check on the marking accuracy for the candidates detailed in the below listed batches. These scripts have been uploaded to your RM Assessor work list or will have been sent in a separate email including the batch number in the subject line. The Mark Input Sheets for these batches can be found on your Secure Exchange account. Your attention is directed to the Instructions and Guidance already issued.</p>

          
        <ul>
        <li>
        When the work has been completed, you should indicate on the Mark Input Sheet whether you have confirmed or changed the mark in the ‘Mark Confirmed’ column.  
        </li>
        <li>
        Please note that the marks provided by Cambridge International are the candidates’ marks after any Examiner scaling has been applied.  
        </li>
        <li>
        If the mark you have awarded is different to that of the original mark stated on the MIS, you should enter any new mark in the ‘Mark for Input if Different’ column. 
        </li>
        <li>
        If entering a new mark, you must also enter the Justification Code in the column provided on the spreadsheet.   
        </li>
        <li>
        Please do not change the name of the file when you download it and upload it to Secure Exchange.   
        </li>
        <li>
        Please upload the completed MIS forms to your Secure Exchange account to return them to us. 
        </li>
        <li>
        Please keep a copy of the candidate’s details where any mark change has been made. 
        </li>
        <li>
        Services 2P and 2PS are priority EAR services. Please prioritize any of these services that are present in your worklist.  
        </li>
        </ul> 

        <h3>Please see below batches assigned to you and the date which they are due for completion. </h3>

        <h3>Worklist; </h3>

        <table id="customers">
          <tr>
            <th>Due Date</th>
            <th>Service</th>
            <th>Batch</th>
            <th>Syllabus/Component</th>
            <th>Centre ID</th>
            <th>Candidate ID</th>
          </tr>
        $table_entry_insert
        </table>

        <h3>RM Assessor scripts may not be available on receipt of this email. Please contact us if they have not appeared within 24 hours of this email being sent. </h3>

        <p>If completion of this work by the required date is not possible, or if you have any queries relating to this request, please contact the Enquiries about Results team on 01223 553771 or via email to results.enquiries@cambridge.org. If the enquiry is not received back by the date stated above, we will be contacting examiners to ensure that they have received the enquiry and not encountered any issues. </p>

        <h3>Enquiries about Results Team  -  Cambridge Assessment International Education</h3>
        <p>Direct: +44 1223 553771 <br>
        Email: results.enquiries@cambridge.org</p>

        <p>The Triangle Building, Shaftesbury Road, Cambridge CB2 8EA, UK <br>
        <b>www.cambridgeinternational.org</b></p>

        <p><b>Cambridge Assessment International Education</b> prepares school students for life, helping them develop an informed curiosity and a lasting passion for learning. We are part of the University of Cambridge. </p>
        </body>
        """)
        HtmlBody_final = HtmlBody.substitute(table_entry_insert=table_entry,full_name=full_name)

        with open(file_location, 'a', newline='') as file:
            file.truncate()
            writer = csv.writer(file)

            script_id = script.ec_sid.ec_sid
            examiner = uc.exm_creditor_no + ' ' + full_name
            email = uc.exm_email

            writer.writerow([script_id,examiner,email])
