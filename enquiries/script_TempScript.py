import sys
import os
import django
import datetime
import pyodbc
import pandas as pd
from openpyxl import load_workbook


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

from enquiries.models import CentreEnquiryRequests, EnquiryDeadline, ExaminerPanels, UniqueCreditor, EarServerSettings, ScaledMarks, UniqueCreditor, ExaminerAvailability, ExaminerNotes, ExaminerConflicts
from django.contrib.auth.models import User

#Limits enquiries to session or enquiry list
session_id = EarServerSettings.objects.first().session_id_list
enquiry_id_list = EarServerSettings.objects.first().enquiry_id_list
if enquiry_id_list != '':
    enquiry_id_list = ' and sid in (' + enquiry_id_list + ')'

print("ENQ:" + enquiry_id_list)

filename=os.path.join("Y:\Operations\Results Team\Enquiries About Results\\0.Nova Downloads\\exm_avail.xlsx")
workbook = load_workbook(filename)
sheet = workbook.active

ExaminerConflicts.objects.all().delete()

for row in sheet.iter_rows():
    creditor = str(row[3].value)
    avail_ind = str(row[6].value)
    avail_string = str(row[7].value).split(',')
    conflict = str(row[8].value)
    notes = str(row[9].value)

    

    if UniqueCreditor.objects.filter(exm_creditor_no=creditor).exists():
    #     if notes != 'None':
    #         exm = UniqueCreditor.objects.get(exm_creditor_no=creditor)
    #         note_entry = ExaminerNotes(
    #             examiner_notes = notes,
    #             note_owner = User.objects.get(username='NovaServer'),
    #         )
    #         note_entry.save()
    #         note_entry.creditor.add(exm)

        if conflict != 'No Conflict of Interest':
            print(notes)
            exm = UniqueCreditor.objects.get(exm_creditor_no=creditor)
            conflict_entry = ExaminerConflicts(
            examiner_conflicts = conflict,
            note_owner = User.objects.get(username='NovaServer'),
            )
            conflict_entry.save()
            conflict_entry.creditor.add(exm)

        # if avail_ind == 'Partly Available':
        #     for ava in avail_string:
        #         ava = str(ava).strip()
        #         ava_final = ava.split('-')
        #         ava_start = ava_final[0]
        #         ava_finish = 'None'
        #         if ava_start != 'None':
        #             s = ava_final[0]
        #             ava_start = '2023'+'-'+s[3:]+'-'+s[:2]
        #             try:
        #                 s = ava_final[1]
        #                 ava_finish = '2023'+'-'+s[3:]+'-'+s[:2]
        #             except IndexError:
        #                 ava_finish = ava_start
        #                 pass

        #             exm = UniqueCreditor.objects.get(exm_creditor_no=creditor)
        #             avail = ExaminerAvailability(
        #             #ea_sid = models.EnquiryPersonnel.objects.only('enpe_sid').get(enpe_sid=enpe_sid),
        #             unavailability_start_date = ava_start,
        #             unavailability_end_date = ava_finish,
        #             unavailable_2_flag = 'N',
        #             unavailable_5_flag = 'N',
        #             unavailable_9_flag = 'N',
        #             )
        #             avail.save()
        #             avail.creditor.add(exm)

        # elif avail_ind == 'Not Available':
        #     exm = UniqueCreditor.objects.get(exm_creditor_no=creditor)
        #     avail = ExaminerAvailability(
        #     #ea_sid = models.EnquiryPersonnel.objects.only('enpe_sid').get(enpe_sid=enpe_sid),
        #     unavailability_start_date = '2023-08-10',
        #     unavailability_end_date = '2023-10-20',
        #     unavailable_2_flag = 'N',
        #     unavailable_5_flag = 'N',
        #     unavailable_9_flag = 'N',
        #     )
        #     avail.save()
        #     avail.creditor.add(exm)
    else:
        print(creditor)

print("EC loaded:" + str(datetime.datetime.now()))