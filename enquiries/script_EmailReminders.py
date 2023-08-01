
# from email.message import EmailMessage
# import smtplib

# sender = "sender@outlook.com"
# recipient = "recipient@example.com"
# message = "Hello world!"

# email = EmailMessage()
# email["From"] = sender
# email["To"] = recipient
# email["Subject"] = "Test Email"
# email.set_content(message)

# smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
# smtp.starttls()
# smtp.login(sender, "my_outlook_password_123")
# smtp.sendmail(sender, recipient, email.as_string())
# smtp.quit()




import win32com.client as win32

outlook = win32.Dispatch('outlook.application')

mail = outlook.CreateItem(0)
mail.To = 'jacob.bulman@cambridge.org'
mail.Subject = 'Enquiry About Results – Review of Marking Worklist '
mail.HtmlBody = """

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
<p>Dear Mr Jake Bulman</p>

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
  </tr>
  <tr>
    <td>02/08/2023</td>
    <td>2S</td>
    <td>123456</td>
    <td>0400/02</td>
  </tr>
  <tr>
    <td>02/08/2023</td>
    <td>2P</td>
    <td>234567</td>
    <td>9654/08</td>
  </tr>
  <tr>
    <td>03/08/2023</td>
    <td>2</td>
    <td>345678</td>
    <td>6543/21</td>
  </tr>
</table>
 
<h3>RM Assessor scripts may not be available on receipt of this email. Please contact us if they have not appeared within 12 hours of this email being sent. </h3>

<p>If completion of this work by the required date is not possible, or if you have any queries relating to this request, please contact the Enquiries about Results team on 01223 553771 or via email to results.enquiries@cambridge.org. If the enquiry is not received back by the date stated above, we will be contacting examiners to ensure that they have received the enquiry and not encountered any issues. </p>

<h3>Enquiries about Results Team  -  Cambridge Assessment International Education</h3>
<p>Direct: +44 1223 553771 <br>
Email: results.enquiries@cambridge.org</p>

<p>The Triangle Building, Shaftesbury Road, Cambridge CB2 8EA, UK <br>
<b>www.cambridgeinternational.org</b></p>

<p><b>Cambridge Assessment International Education</b> prepares school students for life, helping them develop an informed curiosity and a lasting passion for learning. We are part of the University of Cambridge. </p>
</body>
 """
mail.Send()