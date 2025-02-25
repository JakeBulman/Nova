try:
    from openpyxl import load_workbook
    import sys
    import os
    import django
    from django.utils import timezone
    import datetime
    from string import Template

    from django.conf import settings
    import csv, os, time

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

    from enquiries.models import MailingList, MailingListScripts
    from email.message import EmailMessage
    import smtplib

    #Get and loop through each mailing list item
    all_mailing_lists = MailingList.objects.filter(send_date=datetime.date.today(),email_sent=0)

    for mailing_list in all_mailing_lists:
        try:
            time.sleep(3)
            #Get each script item and add to the html table
            
            table_entry = ''
            mailing_list_scripts = MailingListScripts.objects.filter(mailing_list=mailing_list.pk).order_by('due_date')
            for mailing_list_script in mailing_list_scripts:
                table_entry = table_entry + f"""
                <tr>
                <td>{mailing_list_script.due_date}</td>
                <td>{mailing_list_script.service_code}</td>
                <td>{mailing_list_script.eb_sid.eb_sid}</td>
                <td>{mailing_list_script.syll_comp}</td>
                <td>{mailing_list_script.centre_id}</td>
                <td>{mailing_list_script.candidate_id}</td>
                </tr>
                """
            #Update main html template for email body
                            
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

            <p>We have been asked to provide a check on the marking accuracy for the candidates detailed in the below listed batches. These scripts have been uploaded to your RM Assessor work list or will have been sent in a separate email including the batch number in the subject line. The Mark Input Sheets for these batches can be found on your Secure Exchange account. Please note that for March 2024 ‘NEW’ and revised sections are available in ‘Enquiries about Results Instructions for examiners marking on screen’. Your attention is directed to the Instructions and Guidance already issued, but for ease of access here is a brief bullet point summary of the process:</p>
                                
            <ol>
            <li>
            Receive this email and review outstanding batches listed under Worklist      
            </li>                  
            <li>
            Find batch in Secure Exchange folder /CI/EAR/Examiners/Examiner-(your examiner number). Secure Exchange: https://exchange.cambridgeinternational.org/human.aspx?r=2137397631&arg12=home                       
            </li> 
            <li>
            Download batch     
            </li> 
            <li>
            Open RM and locate script on the batch  
            </li> 
            <li>
            Mark script on RM and submit. Populate MIS.     
            </li> 
            <li>
            Upload completed MIS to folder /CI/EAR/ReturntoCI/Examiner-(your examiner number)     
            </li>           
            </ol>

            <p>Please note, some of the batches listed below you may have already completed and therefore can be ignored if you have already returned the work to us. MIS are processed at four key times in the day from Secure Exchange so any changes can take a few hours to be reflected in your worklist.</p>
            
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
            Please upload the completed MIS forms to your ReturnToCI folder within your Secure Exchange account to return them to us.   
            </li>
            <li>
            Please keep a copy of the candidate’s details where any mark change has been made. 
            </li>
            <li>
            Services 2P and 2PS are priority EAR services. Please prioritize any of these services that are present in your worklist.  
            </li>
            <li>
            SEAB are priority enquiries and examiners are asked to return work within 2 days.  
            </li>
            </ul> 

            <h3>Please see below batches assigned to you and the date which they are due for completion. Please work through the list from top to bottom. </h3>

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

            <h3>RM Assessor scripts may not be available on receipt of this email. Please contact us if they have not appeared within 12 hours of this email being sent. </h3>
            <h3>Additionally, if you have returned batches to us and the due date has passed please contact us using the details below.  </h3>

            <p>If completion of this work by the required date is not possible, or if you have any queries relating to this request, please contact the Enquiries about Results team on 01223 553771 or via email to results.enquiries@cambridge.org. If the enquiry is not received back by the date stated above, we will be contacting examiners to ensure that they have received the enquiry and not encountered any issues. </p>

            <h3>Enquiries about Results Team  -  Cambridge Assessment International Education</h3>
            <p>Direct: +44 1223 553771 <br>
            Email: results.enquiries@cambridge.org</p>

            <p>The Triangle Building, Shaftesbury Road, Cambridge CB2 8EA, UK <br>
            <b>www.cambridgeinternational.org</b></p>

            <p><b>Cambridge Assessment International Education</b> prepares school students for life, helping them develop an informed curiosity and a lasting passion for learning. We are part of the University of Cambridge. </p>
            </body>
            """)
            HtmlBody_final = HtmlBody.substitute(table_entry_insert=table_entry,full_name=mailing_list.email_name)


            #send email to mailing list address, set email_sent to 1

            sender = "results.enquiries@cambridge.org"
            #recipient = mailing_list.email_address
            recipient = "jacob.bulman@cambridge.org"

            email = EmailMessage()
            email["From"] = sender
            email["To"] = recipient
            email["Subject"] = "Enquiry About Results – Review of Marking Worklist"
            email.set_content(HtmlBody_final, subtype='html')
            smtp = smtplib.SMTP("smtp0.ucles.internal", port=25) 
            smtp.sendmail(sender, recipient, email.as_string())
            smtp.quit()

            mailing_list.objects.update(email_sent=1)
            print('SENT TO:' + recipient)
        except Exception as e:
            print(e)
        #Send success/failure email

    email = EmailMessage()
    email["From"] = "results.enquiries@cambridge.org"
    email["To"] = "results.enquiries@cambridge.org, jacob.bulman@cambridge.org,ben.herbert@cambridge.org,charlotte.weedon@cambridge.org,lab.d@cambridgeassessment.org.uk"
    email["Subject"] = "Review of Marking Worklist Emails - Sent Successfully"
    email.set_content("All emails have been sent successfully", subtype='html')

    smtp = smtplib.SMTP("smtp0.ucles.internal", port=25) 
    smtp.sendmail(sender, ["results.enquiries@cambridge.org", "jacob.bulman@cambridge.org","ben.herbert@cambridge.org","charlotte.weedon@cambridge.org","lab.d@cambridgeassessment.org.uk"], email.as_string())
    smtp.quit()

    print('Finished Successfully')
except Exception as e:
    sender = "results.enquiries@cambridge.org"
    email = EmailMessage()
    email["From"] = "results.enquiries@cambridge.org"
    email["To"] = "results.enquiries@cambridge.org, jacob.bulman@cambridge.org,,ben.herbert@cambridge.org,charlotte.weedon@cambridge.org,lab.d@cambridgeassessment.org.uk"
    email["Subject"] = "Review of Marking Worklist Emails - ERROR"
    email.set_content(f"Emails have not been sent successfully, please contact the system administrator for further details. {e}", subtype='html')

    smtp = smtplib.SMTP("smtp0.ucles.internal", port=25) 
    smtp.sendmail(sender, ["results.enquiries@cambridge.org", "jacob.bulman@cambridge.org","ben.herbert@cambridge.org","charlotte.weedon@cambridge.org","lab.d@cambridgeassessment.org.uk"], email.as_string())
    smtp.quit()

    print('Did not finish')
    print(e)