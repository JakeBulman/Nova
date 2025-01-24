									
import sys									
import os									
import django									
from django.utils import timezone									
import datetime									
									
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
									
from enquiries.models import TaskManager, EnquiryComponents, CentreEnquiryRequests, EnquiryComponentsHistory, EnquiryComponentElements,MisReturnData,EnquiryBatches,EnquiryPersonnelDetails,ScriptApportionment,TaskTypes,EnquiryComponentsExaminerChecks,EnquiryComponentsPreviousExaminers
from django.contrib.auth.models import User									
									
enquiry_list = [									
		'1358486',
'1358602',
'1359246',
'1359306',
'1359308',
'1359312',
'1359312',
'1359574',
'1359666',
'1359736',
'1359914',
'1359932',
'1362642',
'1363210',
'1363914',
'1364058',
'1364280',
'1364384',
'1364546',
'1364938',
'1364942',
'1365002',
'1365690',
'1366372',
'1367592',
'1367912',
'1367926',
'1367956',
'1368170',
'1368184',
'1368232',
'1368266',
'1368382',
'1368392',
'1369232',
							
    ]									
									
for enquiry_id in enquiry_list:									
		all_initch = TaskManager.objects.filter(task_id='INITCH',task_completion_date__isnull=True,enquiry_id__enquiries__enquiry_parts__isnull=False, enquiry_id=enquiry_id)							
		for task in all_initch:							
			print(task.enquiry_id.enquiry_id)						
			enquiry_id = task.enquiry_id.enquiry_id						
					#Get scripts for this enquiry ID, this is a join from EC to ERP				
			Scripts = EnquiryComponents.objects.filter(erp_sid__cer_sid = enquiry_id)						
			for s in Scripts:						
				#Check for pre-emptive scaled marks					
				if EnquiryComponentsHistory.objects.filter(ec_sid=s.ec_sid).exists():					
					kbr = EnquiryComponentsHistory.objects.filter(ec_sid=s.ec_sid).first().kbr_code				
				else:					
					kbr = None				
				if kbr == 'SM' and s.erp_sid.cer_sid.ministry_flag == 'MU':					
					#Create confirmed MIS				
					print('SM')				
					eb_sid = EnquiryComponentElements.objects.get(ec_sid=s.ec_sid).eb_sid.eb_sid				
					if MisReturnData.objects.filter(ec_sid=s.ec_sid).exists():				
						MisReturnData.objects.filter(ec_sid=s.ec_sid).update(			
							eb_sid = EnquiryBatches.objects.get(eb_sid=eb_sid),		
							ec_sid = EnquiryComponents.objects.get(ec_sid=s.ec_sid),		
							original_exm = None,		
							rev_exm = '01.01',		
							original_mark = None,		
							mark_status = 'Confirmed',		
							revised_mark = 0,		
							justification_code = None,		
							remark_reason = None,		
							remark_concern_reason = None		
						)			
					else:				
						MisReturnData.objects.create(			
							eb_sid = EnquiryBatches.objects.get(eb_sid=eb_sid),		
							ec_sid = EnquiryComponents.objects.get(ec_sid=s.ec_sid),		
							original_exm = None,		
							rev_exm = '01.01',		
							original_mark = None,		
							mark_status = 'Confirmed',		
							revised_mark = 0,		
							justification_code = None,		
							remark_reason = None,		
							remark_concern_reason = None		
						)			
									
					#Assign script to PE				
					try:				
						principal_exm = EnquiryPersonnelDetails.objects.filter(exm_examiner_no='01.01',ass_code=s.eps_ass_code,com_id=s.eps_com_id,enpe_sid__currently_valid=True).first().enpe_sid			
					except:				
						principal_exm = None			
					if ScriptApportionment.objects.filter(ec_sid=s.ec_sid,apportionment_invalidated=0,script_marked=1).exists():				
						print('Script already apportioned')			
					else:				
						ScriptApportionment.objects.create(			
							enpe_sid = principal_exm,		
							ec_sid = s		
							#script_marked is default to 1		
		)							
									
									
					#Create BOTAPP and MKWAIT				
					if not TaskManager.objects.filter(ec_sid=s.ec_sid, task_id='BOTAPP',task_completion_date = None).exists():				
						TaskManager.objects.create(			
						enquiry_id = CentreEnquiryRequests.objects.only('enquiry_id').get(enquiry_id=enquiry_id),			
						ec_sid = EnquiryComponents.objects.only('ec_sid').get(ec_sid=s.ec_sid),			
						task_id = TaskTypes.objects.get(task_id = 'BOTAPP'),			
						task_assigned_to = User.objects.get(username='RPABOT'),			
						task_assigned_date = timezone.now(),			
						task_completion_date = None			
						)			
					if not TaskManager.objects.filter(ec_sid=s.ec_sid, task_id='MKWAIT',task_completion_date = None).exists():				
						TaskManager.objects.create(			
						enquiry_id = CentreEnquiryRequests.objects.only('enquiry_id').get(enquiry_id=enquiry_id),			
						ec_sid = EnquiryComponents.objects.only('ec_sid').get(ec_sid=s.ec_sid),			
						task_id = TaskTypes.objects.get(task_id = 'MKWAIT'),			
						task_assigned_to = User.objects.get(username='NovaServer'),			
						task_assigned_date = timezone.now(),			
						task_completion_date = None			
						)			
					continue				
									
									
				if s.script_type == 'MIC - MU' or s.script_type == 'MIC - SEAB' or s.script_type == 'MIC - BR':					
					if not TaskManager.objects.filter(ec_sid=s.ec_sid, task_id='LOCMAR',task_completion_date = None).exists():				
						TaskManager.objects.create(			
						enquiry_id = CentreEnquiryRequests.objects.only('enquiry_id').get(enquiry_id=enquiry_id),			
						ec_sid = EnquiryComponents.objects.only('ec_sid').get(ec_sid=s.ec_sid),			
						task_id = TaskTypes.objects.get(task_id = 'LOCMAR'),			
						task_assigned_to = None,			
						task_assigned_date = None,			
						task_completion_date = None			
						)			
					continue				
				if s.script_type == 'Multiple Choice':					
					if not TaskManager.objects.filter(ec_sid=s.ec_sid, task_id='OMRCHE',task_completion_date = None).exists():				
						TaskManager.objects.create(			
						enquiry_id = CentreEnquiryRequests.objects.only('enquiry_id').get(enquiry_id=enquiry_id),			
						ec_sid = EnquiryComponents.objects.only('ec_sid').get(ec_sid=s.ec_sid),			
						task_id = TaskTypes.objects.get(task_id = 'OMRCHE'),			
						task_assigned_to = None,			
						task_assigned_date = None,			
						task_completion_date = None			
						)			
					continue				
				if '1' in s.erp_sid.service_code:					
					if not TaskManager.objects.filter(ec_sid=s.ec_sid, task_id='CLERIC',task_completion_date = None).exists():				
						TaskManager.objects.create(			
						enquiry_id = CentreEnquiryRequests.objects.only('enquiry_id').get(enquiry_id=enquiry_id),			
						ec_sid = EnquiryComponents.objects.only('ec_sid').get(ec_sid=s.ec_sid),			
						task_id = TaskTypes.objects.get(task_id = 'CLERIC'),			
						task_assigned_to = None,			
						task_assigned_date = None,			
						task_completion_date = None			
						)			
				else:					
					if EnquiryComponentsExaminerChecks.objects.filter(ec_sid = s.ec_sid).count() > 0:				
						if not TaskManager.objects.filter(ec_sid=s.ec_sid, task_id='PEXMCH',task_completion_date = None).exists():			
							TaskManager.objects.create(		
							enquiry_id = CentreEnquiryRequests.objects.only('enquiry_id').get(enquiry_id=enquiry_id),		
							ec_sid = EnquiryComponents.objects.only('ec_sid').get(ec_sid=s.ec_sid),		
							task_id = TaskTypes.objects.get(task_id = 'PEXMCH'),		
							task_assigned_to = None,		
							task_assigned_date = None,		
							task_completion_date = None		
							)		
					else:				
					#create a new task for the next step (AUTAPP)				
						#if not TaskManager.objects.filter(ec_sid=s.ec_sid, task_id='MANAPP',task_completion_date = None).exists():			
						if not TaskManager.objects.filter(ec_sid=s.ec_sid, task_id='AUTAPP',task_completion_date = None).exists():			
							TaskManager.objects.create(		
								enquiry_id = CentreEnquiryRequests.objects.only('enquiry_id').get(enquiry_id=enquiry_id),	
								ec_sid = EnquiryComponents.objects.only('ec_sid').get(ec_sid=s.ec_sid),	
								#task_id = TaskTypes.objects.get(task_id = 'MANAPP'),	
								task_id = TaskTypes.objects.get(task_id = 'AUTAPP'),	
								task_assigned_to = None,	
								task_assigned_date = None,	
								task_completion_date = None	
							)		
							EnquiryComponentsPreviousExaminers.objects.create(		
								cer_sid = CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),	
								ec_sid = EnquiryComponents.objects.get(ec_sid=s.ec_sid),	
								exm_position = EnquiryComponentsHistory.objects.get(ec_sid=s.ec_sid).exm_position	
							)		
				#complete the task																
			#complete the task						
			TaskManager.objects.filter(enquiry_id=enquiry_id,task_id='INITCH').update(task_completion_date=timezone.now())						
