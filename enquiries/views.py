from django.http import FileResponse
from . import models
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from django.conf import settings
import csv, os
from django.db.models import Sum, Count
from django.contrib.auth.models import User

#special imports
from . import script_ServerResetShort as srs
#from . import script_ServerResetFull as srf

PageNotAnInteger = None
EmptyPage = None

# Create your views here.
@login_required
def ear_home_view(request,*args, **kwargs):
	#return HttpResponse("<h1>Hello World</h1>")
	user = None
	if request.user.is_authenticated:
		user = request.user
	
	mytask_count = models.TaskManager.objects.filter(task_assigned_to=user, task_completion_date__isnull=True)
	cer_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='INITCH', enquiry_tasks__task_completion_date__isnull=True)
	esmcsv_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='ESMCSV', enquiry_tasks__task_completion_date__isnull=True)
	bie_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='SETBIE', enquiry_tasks__task_completion_date__isnull=True)
	bie_count_assigned = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='SETBIE', enquiry_tasks__task_completion_date__isnull=True, enquiry_tasks__task_assigned_to__isnull=False)
	manapp_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='MANAPP', enquiry_tasks__task_completion_date__isnull=True)
	manapp_count_assigned = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='MANAPP', enquiry_tasks__task_completion_date__isnull=True, enquiry_tasks__task_assigned_to__isnull=False)
	botapp_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='BOTAPP', enquiry_tasks__task_completion_date__isnull=True)
	botapp_fail_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='BOTAPF', enquiry_tasks__task_completion_date__isnull=True)
	botmar_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='BOTMAR', enquiry_tasks__task_completion_date__isnull=True)
	botmar_fail_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='BOTMAF', enquiry_tasks__task_completion_date__isnull=True)
	misvrm_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='MISVRM', enquiry_tasks__task_completion_date__isnull=True)
	misvrma_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='MISVRM', enquiry_tasks__task_completion_date__isnull=True, enquiry_tasks__task_assigned_to__isnull=False)
	nrmacc_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='NRMACC', enquiry_tasks__task_completion_date__isnull=True)
	nrmacca_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='NRMACC', enquiry_tasks__task_completion_date__isnull=True, enquiry_tasks__task_assigned_to__isnull=False)
	cleric_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='CLERIC', enquiry_tasks__task_completion_date__isnull=True)
	clerica_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='CLERIC', enquiry_tasks__task_completion_date__isnull=True, enquiry_tasks__task_assigned_to__isnull=False)
	pexmch_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='PEXMCH', enquiry_tasks__task_completion_date__isnull=True)
	pexmcha_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='PEXMCH', enquiry_tasks__task_completion_date__isnull=True, enquiry_tasks__task_assigned_to__isnull=False)
	exmsla_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='EXMSLA', enquiry_tasks__task_completion_date__isnull=True)
	exmslaa_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='EXMSLA', enquiry_tasks__task_completion_date__isnull=True, enquiry_tasks__task_assigned_to__isnull=False)
	grdrel_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='GRDREL', enquiry_tasks__task_completion_date__isnull=True)
	grdrela_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='GRDREL', enquiry_tasks__task_completion_date__isnull=True, enquiry_tasks__task_assigned_to__isnull=False)
	remapp_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='REMAPP', enquiry_tasks__task_completion_date__isnull=True)
	remappa_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='REMAPP', enquiry_tasks__task_completion_date__isnull=True, enquiry_tasks__task_assigned_to__isnull=False)
	remapf_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='REMAPF', enquiry_tasks__task_completion_date__isnull=True)
	remapfa_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='REMAPF', enquiry_tasks__task_completion_date__isnull=True, enquiry_tasks__task_assigned_to__isnull=False)
	negcon_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='NEGCON', enquiry_tasks__task_completion_date__isnull=True)
	negcona_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='NEGCON', enquiry_tasks__task_completion_date__isnull=True, enquiry_tasks__task_assigned_to__isnull=False)
	pdacon_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='PDACON', enquiry_tasks__task_completion_date__isnull=True)
	pdacona_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='PDACON', enquiry_tasks__task_completion_date__isnull=True, enquiry_tasks__task_assigned_to__isnull=False)
	peacon_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='PEACON', enquiry_tasks__task_completion_date__isnull=True)
	peacona_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='PEACON', enquiry_tasks__task_completion_date__isnull=True, enquiry_tasks__task_assigned_to__isnull=False)
	pumcon_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='PUMCON', enquiry_tasks__task_completion_date__isnull=True)
	pumcona_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='PUMCON', enquiry_tasks__task_completion_date__isnull=True, enquiry_tasks__task_assigned_to__isnull=False)
	grdrej_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='GRDREJ', enquiry_tasks__task_completion_date__isnull=True)
	grdreja_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='GRDREJ', enquiry_tasks__task_completion_date__isnull=True, enquiry_tasks__task_assigned_to__isnull=False)
	mrkamd_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='MRKAMD', enquiry_tasks__task_completion_date__isnull=True)
	mrkamda_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='MRKAMD', enquiry_tasks__task_completion_date__isnull=True, enquiry_tasks__task_assigned_to__isnull=False)
	grdcon_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='GRDCON', enquiry_tasks__task_completion_date__isnull=True)
	grdcona_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='GRDCON', enquiry_tasks__task_completion_date__isnull=True, enquiry_tasks__task_assigned_to__isnull=False)
	grdchg_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='GRDCHG', enquiry_tasks__task_completion_date__isnull=True)
	grdchga_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='GRDCHG', enquiry_tasks__task_completion_date__isnull=True, enquiry_tasks__task_assigned_to__isnull=False)
	outcon_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='OUTCON', enquiry_tasks__task_completion_date__isnull=True)
	outcona_count = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='OUTCON', enquiry_tasks__task_completion_date__isnull=True, enquiry_tasks__task_assigned_to__isnull=False)

	session_desc = models.EarServerSettings.objects.first().session_description
	context = {"session_desc":session_desc, "mytask":mytask_count,"cer":cer_count, "bie":bie_count, "biea":bie_count_assigned, "manapp": manapp_count, "manappa": manapp_count_assigned, 
	    "botapp":botapp_count, "botapf":botapp_fail_count, "botmar":botmar_count, "botmaf":botmar_fail_count, "misvrm":misvrm_count, "misvrma":misvrma_count,
		"pexmch":pexmch_count, "pexmcha":pexmcha_count, "cleric":cleric_count, "clerica":clerica_count, "esmcsv":esmcsv_count, "exmsla":exmsla_count, "exmslaa":exmslaa_count, "remapp":remapp_count, "remappa":remappa_count, "remapf":remapf_count, "remapfa":remapfa_count,
		"grdrel":grdrel_count, "grdrela":grdrela_count, "negcon":negcon_count, "negcona":negcona_count, "pdacon":pdacon_count, "pdacona":pdacona_count, 
		"peacon":peacon_count, "peacon":peacona_count, "pumcon":pumcon_count, "pumcona":pumcona_count, "grdrej":grdrej_count, "grdreja":grdreja_count, "mrkamd":mrkamd_count, 
		"mrkamda":mrkamda_count, "grdcon":grdcon_count, "grdcona":grdcona_count, "grdchg":grdchg_count, "grdchga":grdchga_count, "nrmacc":nrmacc_count, "nrmacca":nrmacca_count
		, "outcon":outcon_count, "outcona":outcona_count
		}
	#Get username to filter tasks
	user = None
	if request.user.is_authenticated:
		user = request.user

	user_status = models.TaskUserPrimary.objects.get(task_user_id=user).primary_status

	if user_status == 'CO':
		return render(request, "home_ear_coordinator.html", context=context, )
	elif user_status == 'TL':
		return render(request, "home_ear.html", context=context, )
	elif user_status == 'AD':
		return render(request, "home_ear_admin.html", context=context, )

	return render(request, "home_ear_restricted.html", context=context, )

def server_options_view(request):
	context = {}
	return render(request, "enquiries_server_options.html", context=context)

def server_settings_view(request):
	serv = models.EarServerSettings.objects.first()
	context = {"serv":serv}
	return render(request, "enquiries_server_settings.html", context=context)

def server_settings_update_view(request):
	sessions = request.POST.get('session_id_list')
	enquiries = request.POST.get('enquiry_id_list')
	session_desc = request.POST.get('session_desc')
	
	serv = models.EarServerSettings.objects.first()
	models.EarServerSettings.objects.filter(id=serv.pk).update(session_id_list=sessions,enquiry_id_list=enquiries,session_description=session_desc)
	# models.EarServerSettings.objects.create(
	# 	session_id_list=sessions,
	# 	enquiry_id_list=enquiries
	# )
	serv = models.EarServerSettings.objects.all().first()
	context = {"serv":serv}
	return render(request, "enquiries_server_settings.html", context=context)

def server_short_reset_view(request):
	srs.clear_tables()
	srs.load_core_tables()
	context = {}
	return render(request, "enquiries_server_options.html", context=context)

def server_long_reset_view(request):
# 	srf.clear_tables()
# 	srf.load_core_tables()
		context = {}
		return render(request, "enquiries_server_options.html", context=context)

def my_tasks_view(request):
	#Get username to filter tasks
	user = None
	if request.user.is_authenticated:
		user = request.user
	#Get task objects for this user
	task_queryset = models.TaskManager.objects.filter(task_assigned_to=user,task_completion_date__isnull=True)
	task_count = models.TaskManager.objects.order_by('task_creation_date').filter(task_assigned_to__isnull=True,task_completion_date__isnull=True).exclude(task_id__in=['INITCH','AUTAPP','BOTAPP','NEWMIS','RETMIS','JUSCHE','BOTMAR','GRDMAT','GRDNEG','ESMCSV','ESMSCR','GRDREL','OUTCON']).count()
	context = {"tasks": task_queryset, "task_count": task_count}
	return render(request, "my_tasks.html", context=context)

def task_router_view(request):
	task_type = request.POST.get('task_type')
	task_id = request.POST.get('task_id')
	
	if task_type == "SETBIE":
		return redirect('setbie-task', task_id=task_id)
	if task_type == "MANAPP":
		return redirect('manual-apportionment-task', task_id=task_id)
	if task_type == "NRMACC":
		return redirect('nrmacc-task', task_id=task_id)
	if task_type == "MISVRM":
		return redirect('misvrm-task', task_id=task_id)
	if task_type == "PEXMCH":
		return redirect('pexmch-task', task_id=task_id)
	if task_type == "CLERIC":
		return redirect('cleric-task', task_id=task_id)
	if task_type == "EXMSLA":
		return redirect('exmsla-task', task_id=task_id)
	if task_type == "REMAPP":
		return redirect('remapp-task', task_id=task_id)
	if task_type == "REMAPF":
		return redirect('remapf-task', task_id=task_id)
	if task_type == "BOTAPF":
		return redirect('botapf-task', task_id=task_id)
	if task_type == "BOTMAF":
		return redirect('botmaf-task', task_id=task_id)
	if task_type == "NEGCON":
		return redirect('negcon-task', task_id=task_id)
	if task_type == "PDACON":
		return redirect('pdacon-task', task_id=task_id)
	if task_type == "PEACON":
		return redirect('peacon-task', task_id=task_id)
	if task_type == "PUMCON":
		return redirect('pumcon-task', task_id=task_id)
	if task_type == "GRDREJ":
		return redirect('grdrej-task', task_id=task_id)
	if task_type == "MRKAMD":
		return redirect('mrkamd-task', task_id=task_id)
	if task_type == "GRDCON":
		return redirect('grdcon-task', task_id=task_id)
	if task_type == "GRDCHG":
		return redirect('grdchg-task', task_id=task_id)
	else:
		return redirect('my_tasks')
	


def new_task_view(request):
	#Get username to filter tasks
	username = None
	if request.user.is_authenticated:
		username =request.user
	#Caclulate next task in the queue
	try:
		next_task_id = models.TaskManager.objects.order_by('task_creation_date').filter(task_assigned_to__isnull=True,task_completion_date__isnull=True).exclude(task_id__in=['INITCH','AUTAPP','BOTAPP','NEWMIS','RETMIS','JUSCHE','BOTMAR','GRDMAT','ESMCSV','ESMSCR','GRDREL','OUTCON']).first().pk
	except:
		next_task_id = None
	#Set the newest task to this user
	if next_task_id is not None:
		models.TaskManager.objects.filter(id=next_task_id).update(task_assigned_to=username)
		models.TaskManager.objects.filter(id=next_task_id).update(task_assigned_date=timezone.now())
	return redirect('my_tasks')

def self_assign_task_view(request, task_id=None):
	#Get username to filter tasks
	username = None
	if request.user.is_authenticated:
		username =request.user
	#Set the  task to this user
	print(task_id)
	if task_id is not None:
		models.TaskManager.objects.filter(id=task_id).update(task_assigned_to=username)
		models.TaskManager.objects.filter(id=task_id).update(task_assigned_date=timezone.now())
	redirect_address = request.POST.get('page_location')
	return redirect(redirect_address)

def setbie_task(request, task_id=None):
	task_queryset = models.TaskManager.objects.get(pk=task_id)
	context = {"task_id":task_id, "task":task_queryset}
	return render(request, "enquiries_task_setbie.html", context=context)

def manual_apportionment_task(request, task_id=None):
	task_queryset = models.TaskManager.objects.get(pk=task_id)
	task_ass_code = models.EnquiryComponents.objects.get(script_tasks__pk=task_id).eps_ass_code
	task_comp_code = models.EnquiryComponents.objects.get(script_tasks__pk=task_id).eps_com_id
	examiner_queryset = models.UniqueCreditor.objects.annotate(script_count=Sum("creditors__apportion_examiner__script_marked",distinct=True)).filter(creditors__exm_per_details__ass_code = task_ass_code, creditors__exm_per_details__com_id = task_comp_code).order_by('creditors__exm_per_details__exm_examiner_no')

	#Get task_id for this enquiry if it has SETBIE
	issue_reason = None
	if models.SetIssueAudit.objects.filter(enquiry_id=task_queryset.enquiry_id).exists():
		issue_reason = models.SetIssueAudit.objects.filter(enquiry_id=task_queryset.enquiry_id).first().issue_reason

	context = {"task_id":task_id, "task":task_queryset, "ep":examiner_queryset, "appor_count":0, "issue_reason":issue_reason}
	return render(request, "enquiries_task_manual_apportionment.html", context=context)

def manual_apportionment(request):
	apportion_enpe_sid = request.POST.get('enpe_sid')
	apportion_script_id = request.POST.get('script_id')
	apportion_task_id = request.POST.get('task_id')
	apportion_enquiry_id = request.POST.get('enquiry_id')

	examiner_obj = models.EnquiryPersonnel.objects.get(enpe_sid=apportion_enpe_sid)
	script_obj = models.EnquiryComponents.objects.get(ec_sid=apportion_script_id)

	if not models.ScriptApportionment.objects.filter(enpe_sid=examiner_obj,ec_sid=script_obj).exists():
		models.ScriptApportionment.objects.create(
			enpe_sid = examiner_obj,
			ec_sid = script_obj
			#script_marked is default to 1
		)

	if models.EnquiryComponents.objects.get(ec_sid=apportion_script_id).script_type == "RM Assessor":
		if not models.TaskManager.objects.filter(ec_sid=apportion_script_id, task_id='BOTAPP',task_completion_date = None).exists():
			models.TaskManager.objects.create(
				enquiry_id = models.CentreEnquiryRequests.objects.get(enquiry_id=apportion_enquiry_id),
				ec_sid = models.EnquiryComponents.objects.get(ec_sid=apportion_script_id),
				task_id = models.TaskTypes.objects.get(task_id = 'BOTAPP'),
				task_assigned_to = User.objects.get(username='RPABOT'),
				task_assigned_date = timezone.now(),
				task_completion_date = None
			)
		if not models.TaskManager.objects.filter(ec_sid=apportion_script_id, task_id='NEWMIS',task_completion_date = None).exists():
			models.TaskManager.objects.create(
				enquiry_id = models.CentreEnquiryRequests.objects.get(enquiry_id=apportion_enquiry_id),
				ec_sid = models.EnquiryComponents.objects.get(ec_sid=apportion_script_id),
				task_id = models.TaskTypes.objects.get(task_id = 'NEWMIS'),
				task_assigned_to = User.objects.get(username='NovaServer'),
				task_assigned_date = timezone.now(),
				task_completion_date = None
		)
		if not models.TaskManager.objects.filter(ec_sid=apportion_script_id, task_id='ESMCSV',task_completion_date = None).exists():
			models.TaskManager.objects.create(
				enquiry_id = models.CentreEnquiryRequests.objects.get(enquiry_id=apportion_enquiry_id),
				ec_sid = models.EnquiryComponents.objects.get(ec_sid=apportion_script_id),
				task_id = models.TaskTypes.objects.get(task_id = 'ESMCSV'),
				task_assigned_to = None,
				task_assigned_date = None,
				task_completion_date = None
		)
	else:
		if not models.TaskManager.objects.filter(ec_sid=apportion_script_id, task_id='NRMACC',task_completion_date = None).exists():
			models.TaskManager.objects.create(
				enquiry_id = models.CentreEnquiryRequests.objects.get(enquiry_id=apportion_enquiry_id),
				ec_sid = models.EnquiryComponents.objects.get(ec_sid=apportion_script_id),
				task_id = models.TaskTypes.objects.get(task_id = 'NRMACC'),
				task_assigned_to = None,
				task_assigned_date = None,
				task_completion_date = None
			)		

	#complete the task
	models.TaskManager.objects.filter(pk=apportion_task_id,task_id='MANAPP').update(task_completion_date=timezone.now())    
	return redirect('my_tasks')

def nrmacc_task(request, task_id=None):
	task_queryset = models.TaskManager.objects.get(pk=task_id)
	task_ass_code = models.EnquiryComponents.objects.get(script_tasks__pk=task_id).eps_ass_code
	task_comp_code = models.EnquiryComponents.objects.get(script_tasks__pk=task_id).eps_com_id
	examiner_queryset = models.UniqueCreditor.objects.annotate(script_count=Sum("creditors__apportion_examiner__script_marked",distinct=True)).filter(creditors__exm_per_details__ass_code = task_ass_code, creditors__exm_per_details__com_id = task_comp_code).order_by('creditors__exm_per_details__exm_examiner_no')
	context = {"task_id":task_id, "task":task_queryset, "ep":examiner_queryset,}
	return render(request, "enquiries_task_nrmacc.html", context=context)

def nrmacc_task_complete(request):
	task_id = request.POST.get('task_id')

	apportion_enpe_sid = request.POST.get('enpe_sid')
	apportion_script_id = request.POST.get('script_id')

	task_queryset = models.TaskManager.objects.get(pk=task_id)

	if apportion_enpe_sid:
		examiner_obj = models.EnquiryPersonnel.objects.get(enpe_sid=apportion_enpe_sid)
		script_obj = models.EnquiryComponents.objects.get(ec_sid=apportion_script_id)

		models.ScriptApportionment.objects.filter(ec_sid=script_obj).update(
			enpe_sid = examiner_obj,
		)
		return redirect('nrmacc-task',task_id=task_id)

	else:
		if not models.TaskManager.objects.filter(ec_sid=apportion_script_id, task_id='NEWMIS',task_completion_date = None).exists():
			models.TaskManager.objects.create(
				enquiry_id = models.CentreEnquiryRequests.objects.get(enquiry_id=task_queryset.enquiry_id.enquiry_id),
				ec_sid = models.EnquiryComponents.objects.get(ec_sid=task_queryset.ec_sid.ec_sid),
				task_id = models.TaskTypes.objects.get(task_id = 'NEWMIS'),
				task_assigned_to = User.objects.get(username='NovaServer'),
				task_assigned_date = timezone.now(),
				task_completion_date = None
			)
		#complete the task
		models.TaskManager.objects.filter(pk=task_id,task_id='NRMACC').update(task_completion_date=timezone.now())    
		return redirect('my_tasks')

def misvrm_task(request, task_id=None):
	task_queryset = models.TaskManager.objects.get(pk=task_id)

	#Get task_id for this enquiry if it has SETBIE
	issue_reason = None
	if models.SetIssueAudit.objects.filter(enquiry_id=task_queryset.enquiry_id).exists():
		issue_reason = models.SetIssueAudit.objects.filter(enquiry_id=task_queryset.enquiry_id).first().issue_reason


	context = {"task_id":task_id, "task":task_queryset, "issue_reason":issue_reason}
	return render(request, "enquiries_task_misvrm.html", context=context)

def misvrm_task_complete(request):
	script_id = request.POST.get('script_id')
	task_id = request.POST.get('task_id')
	enquiry_id = request.POST.get('enquiry_id')
	new_mark = request.POST.get('new_mark')
	new_jc = request.POST.get('new_jc')
	new_status = request.POST.get('new_status')

	
	misDataQC = models.MisReturnData.objects.get(ec_sid = script_id)

	if new_mark is None:
		new_mark = misDataQC.revised_mark
		new_jc = misDataQC.justification_code
		new_status = misDataQC.mark_status
	
	models.MisReturnData.objects.filter(ec_sid=script_id).update(final_mark=new_mark)
	models.MisReturnData.objects.filter(ec_sid=script_id).update(final_justification_code=new_jc)
	models.MisReturnData.objects.filter(ec_sid=script_id).update(final_mark_status=new_status)

	if not models.TaskManager.objects.filter(ec_sid=script_id, task_id='JUSCHE',task_completion_date = None).exists():
		models.TaskManager.objects.create(
			enquiry_id = models.CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
			ec_sid = models.EnquiryComponents.objects.get(ec_sid=script_id),
			task_id = models.TaskTypes.objects.get(task_id = 'JUSCHE'),
			task_assigned_to = User.objects.get(username='NovaServer'),
			task_assigned_date = timezone.now(),
			task_completion_date = None
		)

	#complete the task
	models.TaskManager.objects.filter(pk=task_id,task_id='MISVRM').update(task_completion_date=timezone.now())    
	return redirect('my_tasks')


def pexmch_task(request, task_id=None):
	task_queryset = models.TaskManager.objects.get(pk=task_id)
	task_ass_code = models.EnquiryComponents.objects.get(script_tasks__pk=task_id).eps_ass_code
	task_comp_code = models.EnquiryComponents.objects.get(script_tasks__pk=task_id).eps_com_id
	#scripts = models.UniqueCreditor.objects.annotate(script_count=Count("creditors__exm_per_details__enpe_sid__apportion_examiner",distinct=True))
	examiner_queryset = models.UniqueCreditor.objects.filter(creditors__exm_per_details__ass_code = task_ass_code, creditors__exm_per_details__com_id = task_comp_code).order_by('creditors__exm_per_details__exm_examiner_no')
	context = {"task_id":task_id, "task":task_queryset, "ep":examiner_queryset, }
	return render(request, "enquiries_task_pexmch.html", context=context)

def pexmch_task_complete(request):
	script_id = request.POST.get('script_id')
	task_id = request.POST.get('task_id')
	enquiry_id = request.POST.get('enquiry_id')
	exm_1 = request.POST.get('exm_1')
	exm_2 = request.POST.get('exm_2')
	exm_3 = request.POST.get('exm_3')
	exm_4 = request.POST.get('exm_4')
	exm_5 = request.POST.get('exm_5')

	if not models.TaskManager.objects.filter(ec_sid=script_id, task_id='MANAPP',task_completion_date = None).exists():
		if exm_1 != "":
			models.EnquiryComponentsPreviousExaminers.objects.create(
				cer_sid = models.CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
				ec_sid = models.EnquiryComponents.objects.get(ec_sid=script_id),
				exm_position = exm_1
			)
		if exm_2 != "":
			models.EnquiryComponentsPreviousExaminers.objects.create(
				cer_sid = models.CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
				ec_sid = models.EnquiryComponents.objects.get(ec_sid=script_id),
				exm_position = exm_2
			)
		if exm_3 != "":
			models.EnquiryComponentsPreviousExaminers.objects.create(
				cer_sid = models.CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
				ec_sid = models.EnquiryComponents.objects.get(ec_sid=script_id),
				exm_position = exm_3
			)
		if exm_4 != "":
			models.EnquiryComponentsPreviousExaminers.objects.create(
				cer_sid = models.CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
				ec_sid = models.EnquiryComponents.objects.get(ec_sid=script_id),
				exm_position = exm_4
			)
		if exm_5 != "":
			models.EnquiryComponentsPreviousExaminers.objects.create(
				cer_sid = models.CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
				ec_sid = models.EnquiryComponents.objects.get(ec_sid=script_id),
				exm_position = exm_5
			)

		models.TaskManager.objects.create(
			enquiry_id = models.CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
			ec_sid = models.EnquiryComponents.objects.get(ec_sid=script_id),
			#change to AUTAPP once testing complete
			task_id = models.TaskTypes.objects.get(task_id = 'MANAPP'),
			task_assigned_to = None,
			task_assigned_date = None,
			task_completion_date = None
		)

	#complete the task
	models.TaskManager.objects.filter(pk=task_id,task_id='PEXMCH').update(task_completion_date=timezone.now())    
	return redirect('my_tasks')


def cleric_task(request, task_id=None):
	task_queryset = models.TaskManager.objects.get(pk=task_id)
	#Get task_id for this enquiry if it has SETBIE
	issue_reason = None
	if models.SetIssueAudit.objects.filter(enquiry_id=task_queryset.enquiry_id).exists():
		issue_reason = models.SetIssueAudit.objects.filter(enquiry_id=task_queryset.enquiry_id).first().issue_reason

	context = {"task_id":task_id, "task":task_queryset, "issue_reason":issue_reason, }
	return render(request, "enquiries_task_cleric.html", context=context)

def cleric_task_complete(request):
	script_id = request.POST.get('script_id')
	task_id = request.POST.get('task_id')
	enquiry_id = request.POST.get('enquiry_id')
	if script_id is not None and request.method == 'POST':
		enquiry_id = models.TaskManager.objects.filter(ec_sid=script_id,task_id='CLERIC').first().enquiry_id.enquiry_id
		#check if this enquiry already exists at GDWAIT
		gdwait_task = 0
		gdwait_task = models.TaskManager.objects.filter(enquiry_id=enquiry_id,task_id='GDWAIT').count()
		if gdwait_task == 0:
			if not models.TaskManager.objects.filter(enquiry_id=enquiry_id, task_id='GDWAIT',task_completion_date = None).exists():
				models.TaskManager.objects.create(
					enquiry_id = models.CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
					ec_sid = None,
					task_id = models.TaskTypes.objects.get(task_id = 'GDWAIT'),
					task_assigned_to = User.objects.get(username='NovaServer'),
					task_assigned_date = timezone.now(),
					task_completion_date = None
				)
	#complete the task
	models.TaskManager.objects.filter(pk=task_id,task_id='CLERIC').update(task_completion_date=timezone.now())    
	return redirect('my_tasks')


def botapf_task(request, task_id=None):
	task_queryset = models.TaskManager.objects.get(pk=task_id)
	context = {"task_id":task_id, "task":task_queryset, }
	return render(request, "enquiries_task_botapf.html", context=context)

def botapf_task_complete(request):
	task_id = request.POST.get('task_id')
	#complete the task
	models.TaskManager.objects.filter(pk=task_id,task_id='BOTAPF').update(task_completion_date=timezone.now())    
	return redirect('my_tasks')

def botmaf_task(request, task_id=None):
	task_queryset = models.TaskManager.objects.get(pk=task_id)
	context = {"task_id":task_id, "task":task_queryset, }
	return render(request, "enquiries_task_botmaf.html", context=context)

def botmaf_task_complete(request):
	task_id = request.POST.get('task_id')
	script_id = models.TaskManager.objects.get(pk=task_id,task_id='BOTMAF').ec_sid.ec_sid
	if task_id is not None and request.method == 'POST':
		enquiry_id = models.TaskManager.objects.get(pk=task_id,task_id='BOTMAF').enquiry_id.enquiry_id

		#check if this enquiry already exists at GDWAIT
		gdwait_task = 0
		gdwait_task = models.TaskManager.objects.filter(enquiry_id=enquiry_id,task_id='GDWAIT').count()
		if gdwait_task == 0:
			if not models.TaskManager.objects.filter(ec_sid=models.EnquiryComponents.objects.only('ec_sid').get(ec_sid=script_id), task_id='GDWAIT',task_completion_date = None).exists():
				models.TaskManager.objects.create(
					enquiry_id = models.CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
					ec_sid = None,
					task_id = models.TaskTypes.objects.get(task_id = 'GDWAIT'),
					task_assigned_to = User.objects.get(username='NovaServer'),
					task_assigned_date = timezone.now(),
					task_completion_date = None
				)
	#complete the task
	models.TaskManager.objects.filter(pk=task_id,task_id='BOTMAF').update(task_completion_date=timezone.now())    
	models.ScriptApportionment.objects.filter(ec_sid=script_id,script_marked=0,apportionment_invalidated=0).update(script_mark_entered=0)
	return redirect('my_tasks')

def exmsla_task(request, task_id=None):
	task_queryset = models.TaskManager.objects.get(pk=task_id)
	script_id = task_queryset.ec_sid
	extension_total = 0
	for e in models.ScriptApportionmentExtension.objects.filter(task_id=models.TaskManager.objects.get(ec_sid=script_id,task_id='RETMIS').pk):
		extension_total = extension_total + int(e.extenstion_days)
	context = {"task_id":task_id, "task":task_queryset, "ext_days":extension_total }
	return render(request, "enquiries_task_exmsla.html", context=context)

 
def exmsla_task_complete(request):
	script_id = request.POST.get('script_id')
	task_id = request.POST.get('task_id')
	enquiry_id = request.POST.get('enquiry_id')
	new_sla = request.POST.get('new_sla')
	per_sid = request.POST.get('per_sid')
	if new_sla:
		if not models.TaskManager.objects.filter(ec_sid=models.EnquiryComponents.objects.only('ec_sid').get(ec_sid=script_id), task_id='RETMIS',task_completion_date = None).exists():
			models.ScriptApportionmentExtension.objects.create(
				ec_sid = models.EnquiryComponents.objects.get(ec_sid=script_id),
				task_id = models.TaskManager.objects.get(id=models.TaskManager.objects.get(ec_sid=script_id,task_id='RETMIS').pk),
				extenstion_days = new_sla
			)	
			#Recreate RETMIS task (or set to not complete)
			models.TaskManager.objects.filter(pk=models.TaskManager.objects.get(ec_sid=script_id,task_id='RETMIS').pk,task_id='RETMIS').update(
				task_completion_date = None
			)
		models.TaskManager.objects.filter(pk=task_id,task_id='EXMSLA').update(task_completion_date=timezone.now())   
	else:
		if not models.TaskManager.objects.filter(ec_sid=models.EnquiryComponents.objects.only('ec_sid').get(ec_sid=script_id), task_id='REMAPP',task_completion_date = None).exists():
			if task_id:
				models.TaskManager.objects.create(
					enquiry_id = models.CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
					ec_sid = models.EnquiryComponents.objects.get(ec_sid=script_id),
					task_id = models.TaskTypes.objects.get(task_id = 'REMAPP'),
					task_assigned_to = None,
					task_assigned_date = None,
					task_completion_date = None
				)
				#invalidate current apportionement
				models.ScriptApportionment.objects.filter(ec_sid=script_id).update(apportionment_invalidated=1)
				models.TaskManager.objects.filter(pk=task_id,task_id='EXMSLA').update(task_completion_date=timezone.now())   
			else:
				#this is for forced reapportionments
				#close all outstanding tasks
				models.TaskManager.objects.filter(ec_sid=models.EnquiryComponents.objects.get(ec_sid=script_id),task_id__in=['REMAPP','REMAPF','BOTAPP','ESMCSV','NRMACC','EXMSLA','NEWMIS','RETMIS','MISVRM','JUSCHE','MKWAIT','BOTMAR'],task_completion_date=None).update(task_completion_date=timezone.now())
				models.ScriptApportionment.objects.filter(ec_sid=script_id).update(apportionment_invalidated=1)
				#CHECK IF REMAPP ALREADY EXISTS
				models.TaskManager.objects.create(
					enquiry_id = models.CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
					ec_sid = models.EnquiryComponents.objects.get(ec_sid=script_id),
					task_id = models.TaskTypes.objects.get(task_id = 'REMAPP'),
					task_assigned_to = None,
					task_assigned_date = None,
					task_completion_date = None
				)
			return redirect('examiner_scripts',per_sid=per_sid)
			
	return redirect('my_tasks')



def remapp_task(request, task_id=None):
	task_queryset = models.TaskManager.objects.get(pk=task_id)
	task_ass_code = models.EnquiryComponents.objects.get(script_tasks__pk=task_id).eps_ass_code
	task_comp_code = models.EnquiryComponents.objects.get(script_tasks__pk=task_id).eps_com_id
	examiner_queryset = models.UniqueCreditor.objects.annotate(script_count=Sum("creditors__apportion_examiner__script_marked",distinct=True)).filter(creditors__exm_per_details__ass_code = task_ass_code, creditors__exm_per_details__com_id = task_comp_code).order_by('creditors__exm_per_details__exm_examiner_no').exclude(creditors__exm_per_details__enpe_sid__apportion_examiner__apportionment_invalidated=1)

	#Get task_id for this enquiry if it has SETBIE
	issue_reason = None
	if models.SetIssueAudit.objects.filter(enquiry_id=task_queryset.enquiry_id).exists():
		issue_reason = models.SetIssueAudit.objects.filter(enquiry_id=task_queryset.enquiry_id).first().issue_reason

	context = {"task_id":task_id, "task":task_queryset, "ep":examiner_queryset, "appor_count":0, "issue_reason":issue_reason}
	return render(request, "enquiries_task_remapp.html", context=context)

def remapp_task_complete(request):
	apportion_enpe_sid = request.POST.get('enpe_sid')
	apportion_script_id = request.POST.get('script_id')
	apportion_task_id = request.POST.get('task_id')
	apportion_enquiry_id = request.POST.get('enquiry_id')

	examiner_obj = models.EnquiryPersonnel.objects.get(enpe_sid=apportion_enpe_sid)
	script_obj = models.EnquiryComponents.objects.get(ec_sid=apportion_script_id)

	if not models.TaskManager.objects.filter(ec_sid=models.EnquiryComponents.objects.only('ec_sid').get(ec_sid=apportion_script_id), task_id='REMAPF',task_completion_date = None).exists():
		models.ScriptApportionment.objects.create(
			enpe_sid = examiner_obj,
			ec_sid =  script_obj
			#script_marked is default to 1
		)
		models.TaskManager.objects.create(
			enquiry_id = models.CentreEnquiryRequests.objects.get(enquiries__enquiry_parts__ec_sid=apportion_script_id),
			ec_sid = models.EnquiryComponents.objects.get(ec_sid=apportion_script_id),
			task_id = models.TaskTypes.objects.get(task_id = 'REMAPF'),
			task_assigned_to = None,
			task_assigned_date = None,
			task_completion_date = None
		)
		if models.EnquiryComponents.objects.get(ec_sid=apportion_script_id).script_type == "RM Assessor":
			models.TaskManager.objects.create(
				enquiry_id = models.CentreEnquiryRequests.objects.get(enquiry_id=apportion_enquiry_id),
				ec_sid = models.EnquiryComponents.objects.get(ec_sid=apportion_script_id),
				task_id = models.TaskTypes.objects.get(task_id = 'NEWMIS'),
				task_assigned_to = User.objects.get(username='NovaServer'),
				task_assigned_date = timezone.now(),
				task_completion_date = None
			)
			models.TaskManager.objects.create(
				enquiry_id = models.CentreEnquiryRequests.objects.get(enquiry_id=apportion_enquiry_id),
				ec_sid = models.EnquiryComponents.objects.get(ec_sid=apportion_script_id),
				task_id = models.TaskTypes.objects.get(task_id = 'ESMCSV'),
				task_assigned_to = None,
				task_assigned_date = None,
				task_completion_date = None
			)
		else:
			models.TaskManager.objects.create(
				enquiry_id = models.CentreEnquiryRequests.objects.get(enquiry_id=apportion_enquiry_id),
				ec_sid = models.EnquiryComponents.objects.get(ec_sid=apportion_script_id),
				task_id = models.TaskTypes.objects.get(task_id = 'NRMACC'),
				task_assigned_to = None,
				task_assigned_date = None,
				task_completion_date = None
			)		

	#complete the task
	models.TaskManager.objects.filter(pk=apportion_task_id,task_id='REMAPP').update(task_completion_date=timezone.now())    
	return redirect('my_tasks')


def remapf_task(request, task_id=None):
	task_queryset = models.TaskManager.objects.get(pk=task_id)
	task_ass_code = models.EnquiryComponents.objects.get(script_tasks__pk=task_id).eps_ass_code
	task_comp_code = models.EnquiryComponents.objects.get(script_tasks__pk=task_id).eps_com_id
	examiner_queryset = models.UniqueCreditor.objects.annotate(script_count=Sum("creditors__apportion_examiner__script_marked",distinct=True)).filter(creditors__exm_per_details__ass_code = task_ass_code, creditors__exm_per_details__com_id = task_comp_code).order_by('creditors__exm_per_details__exm_examiner_no').exclude(creditors__exm_per_details__enpe_sid__apportion_examiner__apportionment_invalidated=1)

	context = {"task_id":task_id, "task":task_queryset, "ep":examiner_queryset}
	return render(request, "enquiries_task_remapf.html", context=context)

def remapf_task_complete(request):
	apportion_task_id = request.POST.get('task_id')
	#complete the task
	models.TaskManager.objects.filter(pk=apportion_task_id,task_id='REMAPF').update(task_completion_date=timezone.now())    
	return redirect('my_tasks')


def negcon_task(request, task_id=None):
	task_queryset = models.TaskManager.objects.get(pk=task_id)
	context = {"task_id":task_id, "task":task_queryset, }
	return render(request, "enquiries_task_negcon.html", context=context)

def negcon_task_complete(request):
	task_id = request.POST.get('task_id')
	task_status = request.POST.get('task_status')
	enquiry_id = models.TaskManager.objects.get(pk=task_id).enquiry_id.enquiry_id
	if task_status == "Pass":
		if not models.TaskManager.objects.filter(enquiry_id=enquiry_id, task_id='PEACON',task_completion_date = None).exists():
			models.TaskManager.objects.create(
				enquiry_id = models.CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
				ec_sid = None,
				task_id = models.TaskTypes.objects.get(task_id = 'PEACON'),
				task_assigned_to = None,
				task_assigned_date = None,
				task_completion_date = None
			)
	else:
		if not models.TaskManager.objects.filter(enquiry_id=enquiry_id, task_id='GRDREJ',task_completion_date = None).exists():
			models.TaskManager.objects.create(
				enquiry_id = models.CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
				ec_sid = None,
				task_id = models.TaskTypes.objects.get(task_id = 'GRDREJ'),
				task_assigned_to = None,
				task_assigned_date = None,
				task_completion_date = None
			)
			models.GradeFailureAudit.objects.create(
				task_key = models.TaskManager.objects.get(pk=task_id),
				failure_reason = request.POST.get('rpa_fail')
			)		
	#complete the task
	models.TaskManager.objects.filter(pk=task_id,task_id='NEGCON').update(task_completion_date=timezone.now())    
	return redirect('my_tasks')

def peacon_task(request, task_id=None):
	task_queryset = models.TaskManager.objects.get(pk=task_id)
	context = {"task_id":task_id, "task":task_queryset, }
	return render(request, "enquiries_task_peacon.html", context=context)

def peacon_task_complete(request):
	task_id = request.POST.get('task_id')
	task_status = request.POST.get('task_status')
	enquiry_id = models.TaskManager.objects.get(pk=task_id).enquiry_id.enquiry_id
	if task_status == "Pass":
		if not models.TaskManager.objects.filter(enquiry_id=enquiry_id, task_id='PDACON',task_completion_date = None).exists():
			models.TaskManager.objects.create(
				enquiry_id = models.CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
				ec_sid = None,
				task_id = models.TaskTypes.objects.get(task_id = 'PDACON'),
				task_assigned_to = None,
				task_assigned_date = None,
				task_completion_date = None
			)
	else:
		if not models.TaskManager.objects.filter(enquiry_id=enquiry_id, task_id='GRDREJ',task_completion_date = None).exists():
			models.TaskManager.objects.create(
				enquiry_id = models.CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
				ec_sid = None,
				task_id = models.TaskTypes.objects.get(task_id = 'GRDREJ'),
				task_assigned_to = None,
				task_assigned_date = None,
				task_completion_date = None
			)	
			models.GradeFailureAudit.objects.create(
				task_key = models.TaskManager.objects.get(pk=task_id),
				failure_stage = models.TaskTypes.objects.get(task_id='NEGCON'),
				failure_reason = request.POST.get('rpa_fail')
			)
	#complete the task
	models.TaskManager.objects.filter(pk=task_id,task_id='PEACON').update(task_completion_date=timezone.now())    
	return redirect('my_tasks')

def pdacon_task(request, task_id=None):
	task_queryset = models.TaskManager.objects.get(pk=task_id)
	context = {"task_id":task_id, "task":task_queryset, }
	return render(request, "enquiries_task_pdacon.html", context=context)

def pdacon_task_complete(request):
	task_id = request.POST.get('task_id')
	task_status = request.POST.get('task_status')
	enquiry_id = models.TaskManager.objects.get(pk=task_id).enquiry_id.enquiry_id
	if task_status == "Pass":
		if not models.TaskManager.objects.filter(enquiry_id=enquiry_id, task_id='GRDCHG',task_completion_date = None).exists():
			models.TaskManager.objects.create(
				enquiry_id = models.CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
				ec_sid = None,
				task_id = models.TaskTypes.objects.get(task_id = 'GRDCHG'),
				task_assigned_to = None,
				task_assigned_date = None,
				task_completion_date = None
			)
	else:
		if not models.TaskManager.objects.filter(enquiry_id=enquiry_id, task_id='GRDREJ',task_completion_date = None).exists():
			models.TaskManager.objects.create(
				enquiry_id = models.CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
				ec_sid = None,
				task_id = models.TaskTypes.objects.get(task_id = 'GRDREJ'),
				task_assigned_to = None,
				task_assigned_date = None,
				task_completion_date = None
			)	
			models.GradeFailureAudit.objects.create(
				task_key = models.TaskManager.objects.get(pk=task_id),
				failure_reason = request.POST.get('rpa_fail')
			)
	#complete the task
	models.TaskManager.objects.filter(pk=task_id,task_id='PDACON').update(task_completion_date=timezone.now())    
	return redirect('my_tasks')

def pumcon_task(request, task_id=None):
	task_queryset = models.TaskManager.objects.get(pk=task_id)
	context = {"task_id":task_id, "task":task_queryset, }
	return render(request, "enquiries_task_pumcon.html", context=context)

def pumcon_task_complete(request):
	task_id = request.POST.get('task_id')
	task_status = request.POST.get('task_status')
	enquiry_id = models.TaskManager.objects.get(pk=task_id).enquiry_id.enquiry_id
	if task_status == "Pass":
		if not models.TaskManager.objects.filter(enquiry_id=enquiry_id, task_id='COMPLT',task_completion_date = None).exists():
			models.TaskManager.objects.create(
				enquiry_id = models.CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
				ec_sid = None,
				task_id = models.TaskTypes.objects.get(task_id = 'COMPLT'),
				task_assigned_to = None,
				task_assigned_date = None,
				task_completion_date = None
			)
	#complete the task
	models.TaskManager.objects.filter(pk=task_id,task_id='PUMCON').update(task_completion_date=timezone.now())    
	return redirect('my_tasks')

def grdrej_task(request, task_id=None):
	task_queryset = models.TaskManager.objects.get(pk=task_id)
	context = {"task_id":task_id, "task":task_queryset, }
	return render(request, "enquiries_task_grdrej.html", context=context)

def grdrej_task_complete(request):
	task_id = request.POST.get('task_id')
	task_status = request.POST.get('task_status')
	enquiry_id = models.TaskManager.objects.get(pk=task_id).enquiry_id.enquiry_id
	# if task_status == "Pass":
	if not models.TaskManager.objects.filter(enquiry_id=enquiry_id, task_id='MRKAMD',task_completion_date = None).exists():
		models.TaskManager.objects.create(
			enquiry_id = models.CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
			ec_sid = None,
			task_id = models.TaskTypes.objects.get(task_id = 'MRKAMD'),
			task_assigned_to = None,
			task_assigned_date = None,
			task_completion_date = None
		)
		# models.TaskManager.objects.create(
		# 	enquiry_id = models.CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
		# 	ec_sid = None,
		# 	task_id = models.TaskTypes.objects.get(task_id = 'ESMSCR'),
		# 	task_assigned_to = None,
		# 	task_assigned_date = None,
		# 	task_completion_date = None
		# )
	#complete the task
	models.TaskManager.objects.filter(pk=task_id,task_id='GRDREJ').update(task_completion_date=timezone.now())    
	return redirect('my_tasks')

def mrkamd_task(request, task_id=None):
	task_queryset = models.TaskManager.objects.get(pk=task_id)
	context = {"task_id":task_id, "task":task_queryset, }
	return render(request, "enquiries_task_mrkamd.html", context=context)

def mrkamd_task_complete(request):
	task_id = request.POST.get('task_id')
	task_status = request.POST.get('task_status')
	enquiry_id = models.TaskManager.objects.get(pk=task_id).enquiry_id.enquiry_id
	if not models.TaskManager.objects.filter(enquiry_id=enquiry_id, task_id='PUMMAT',task_completion_date = None).exists():
		models.TaskManager.objects.create(
			enquiry_id = models.CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
			ec_sid = None,
			task_id = models.TaskTypes.objects.get(task_id = 'PUMMAT'),
			task_assigned_to = None,
			task_assigned_date = None,
			task_completion_date = None
		)
	#complete the task
	models.TaskManager.objects.filter(pk=task_id,task_id='MRKAMD').update(task_completion_date=timezone.now())    
	return redirect('my_tasks')

def grdcon_task(request, task_id=None):
	task_queryset = models.TaskManager.objects.get(pk=task_id)
	context = {"task_id":task_id, "task":task_queryset, }
	return render(request, "enquiries_task_grdcon.html", context=context)

def grdcon_task_complete(request):
	task_queryset = models.TaskManager.objects.filter(task_id='GRDCON', task_completion_date__isnull=True)
	if task_queryset.count() > 0:
		for t in task_queryset:
			enquiry_id = t.enquiry_id.enquiry_id
			models.TaskManager.objects.create(
                enquiry_id = models.CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
                ec_sid = None,
                task_id = models.TaskTypes.objects.get(task_id = 'OUTCON'),
                task_assigned_to = User.objects.get(username='NovaServer'),
                task_assigned_date = timezone.now(),
                task_completion_date = None
            )

			#Get username to filter tasks
			username = None
			if request.user.is_authenticated:
				username =request.user
			
			models.TaskManager.objects.filter(enquiry_id=t.enquiry_id.enquiry_id,task_id='GRDCON').update(task_completion_date=timezone.now())
			models.TaskManager.objects.filter(enquiry_id=t.enquiry_id.enquiry_id,task_id='GRDCON').update(task_assigned_date=timezone.now())
			models.TaskManager.objects.filter(enquiry_id=t.enquiry_id.enquiry_id,task_id='GRDCON').update(task_assigned_to=username)

	return redirect('enquiries_home')

def grdchg_task(request, task_id=None):
	task_queryset = models.TaskManager.objects.get(pk=task_id)
	context = {"task_id":task_id, "task":task_queryset, }
	return render(request, "enquiries_task_grdchg.html", context=context)

def grdchg_task_complete(request):
	task_id = request.POST.get('task_id')
	task_status = request.POST.get('task_status')
	enquiry_id = models.TaskManager.objects.get(pk=task_id).enquiry_id.enquiry_id
	if task_status == "Pass":
		if not models.TaskManager.objects.filter(enquiry_id=enquiry_id, task_id='OUTCON',task_completion_date = None).exists():
			models.TaskManager.objects.create(
				enquiry_id = models.CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
				ec_sid = None,
				task_id = models.TaskTypes.objects.get(task_id = 'OUTCON'),
				task_assigned_to = None,
				task_assigned_date = None,
				task_completion_date = None
			)
	#complete the task
	models.TaskManager.objects.filter(pk=task_id,task_id='GRDCHG').update(task_completion_date=timezone.now())    
	return redirect('my_tasks')

def outcon_create_view(request):
	task_queryset = models.TaskManager.objects.filter(task_id='OUTCON', task_completion_date__isnull=True)
	if task_queryset.count() > 0:
		for t in task_queryset:
			enquiry_id = t.enquiry_id.enquiry_id
			models.TaskManager.objects.create(
                enquiry_id = models.CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
                ec_sid = None,
                task_id = models.TaskTypes.objects.get(task_id = 'PUMMAT'),
                task_assigned_to = User.objects.get(username='NovaServer'),
                task_assigned_date = timezone.now(),
                task_completion_date = None
            )

			#Get username to filter tasks
			username = None
			if request.user.is_authenticated:
				username =request.user
			
			models.TaskManager.objects.filter(enquiry_id=t.enquiry_id.enquiry_id,task_id='OUTCON').update(task_completion_date=timezone.now())
			models.TaskManager.objects.filter(enquiry_id=t.enquiry_id.enquiry_id,task_id='OUTCON').update(task_assigned_date=timezone.now())
			models.TaskManager.objects.filter(enquiry_id=t.enquiry_id.enquiry_id,task_id='OUTCON').update(task_assigned_to=username)

	return redirect('enquiries_home')

def complete_bie_view(request, enquiry_id=None):
	if enquiry_id is not None and request.method == 'GET':
		t_check = models.TaskManager.objects.filter(enquiry_id=enquiry_id,task_id='SETBIE').update(task_completion_date=timezone.now())
		print(t_check)
	return redirect('my_tasks')

def enquiries_detail(request, enquiry_id=None):
	cer_queryset = None
	if enquiry_id is not None:	
		cer_queryset = models.CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id)
		task_queryset = models.TaskManager.objects.filter(enquiry_id=enquiry_id).order_by('task_creation_date')
		#Get task_id for this enquiry if it has SETBIE
		bie_task_id = None
		if models.TaskManager.objects.filter(task_id='SETBIE',enquiry_id=enquiry_id).exists():
			bie_task_id = models.TaskManager.objects.filter(task_id='SETBIE',enquiry_id=enquiry_id).first().task_id
		#Get task_id for this enquiry if it has SETBIE
		issue_reason = None
		if models.SetIssueAudit.objects.filter(enquiry_id=enquiry_id).exists():
			issue_reason = models.SetIssueAudit.objects.filter(enquiry_id=enquiry_id).first().issue_reason
	context = {"cer": cer_queryset, "bie_status": bie_task_id, "issue_reason":issue_reason, "tasks":task_queryset}
	return render(request, "enquiries_detail.html", context=context)

def enquiries_detail_search(request, id=None):
	enquiry_obj = None
	if request.method == "POST" and 'enquiry_id' in request.POST:
		enquiry_id = request.POST.get('enquiry_id')
		enquiry_obj = models.CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id)
		print(enquiry_obj)
	return redirect('enquiries_detail', enquiry_id)

def enquiries_list_view(request):
	# grab the model rows (ordered by id), filter to required task and where not completed.
	search_q = ""
	if request.GET.get('search_query') is not None:
		search_q = request.GET.get('search_query')
	cer_queryset = models.CentreEnquiryRequests.objects.filter(Q(enquiry_id__icontains = search_q), enquiry_tasks__task_id='INITCH', enquiry_tasks__task_completion_date__isnull=True).order_by('enquiry_id')
	cer_queryset_paged = Paginator(cer_queryset,10,0,True)
	page_number = request.GET.get('page')
	try:
		page_obj = cer_queryset_paged.get_page(page_number)  # returns the desired page object
	except PageNotAnInteger:
		# if page_number is not an integer then assign the first page
		page_obj = cer_queryset_paged.page(1)
	except EmptyPage:
		# if page is empty then return last page
		page_obj = cer_queryset_paged.page(cer_queryset_paged.num_pages)	
	context = {"cer": page_obj, "sq":search_q, }
	return render(request, "enquiries_list.html", context=context)

def enquiries_bie_view(request):
	# grab the model rows (ordered by id), filter to required task and where not completed.
	ec_queryset = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='SETBIE', enquiry_tasks__task_completion_date__isnull=True).order_by('enquiry_id')
	ec_queryset_paged = Paginator(ec_queryset,10,0,True)
	page_number = request.GET.get('page')
	try:
		page_obj = ec_queryset_paged.get_page(page_number)  # returns the desired page object
	except PageNotAnInteger:
		# if page_number is not an integer then assign the first page
		page_obj = ec_queryset_paged.page(1)
	except EmptyPage:
		# if page is empty then return last page
		page_obj = ec_queryset_paged.page(ec_queryset_paged.num_pages)	
	context = {"cer": page_obj,}
	return render(request, "enquiries_list_setbie.html", context=context)

def iec_pass_view(request, enquiry_id=None):
	if enquiry_id is not None and request.method == 'POST':
		#Get scripts for this enquiry ID, this is a join from EC to ERP
		Scripts = models.EnquiryComponents.objects.filter(erp_sid__cer_sid = enquiry_id)
		for s in Scripts:
			if '1' in s.erp_sid.service_code:
				if not models.TaskManager.objects.filter(ec_sid=s.ec_sid, task_id='CLERIC',task_completion_date = None).exists():
					models.TaskManager.objects.create(
					enquiry_id = models.CentreEnquiryRequests.objects.only('enquiry_id').get(enquiry_id=enquiry_id),
					ec_sid = models.EnquiryComponents.objects.only('ec_sid').get(ec_sid=s.ec_sid),
					task_id = models.TaskTypes.objects.get(task_id = 'CLERIC'),
					task_assigned_to = None,
					task_assigned_date = None,
					task_completion_date = None
					)
			else:
				if models.EnquiryComponentsExaminerChecks.objects.filter(ec_sid = s.ec_sid).count() > 0:
					if not models.TaskManager.objects.filter(ec_sid=s.ec_sid, task_id='PEXMCH',task_completion_date = None).exists():
						models.TaskManager.objects.create(
						enquiry_id = models.CentreEnquiryRequests.objects.only('enquiry_id').get(enquiry_id=enquiry_id),
						ec_sid = models.EnquiryComponents.objects.only('ec_sid').get(ec_sid=s.ec_sid),
						task_id = models.TaskTypes.objects.get(task_id = 'PEXMCH'),
						task_assigned_to = None,
						task_assigned_date = None,
						task_completion_date = None
						)
				else:
				#create a new task for the next step (AUTAPP)
					if not models.TaskManager.objects.filter(ec_sid=s.ec_sid, task_id='MANAPP',task_completion_date = None).exists():
						models.TaskManager.objects.create(
							enquiry_id = models.CentreEnquiryRequests.objects.only('enquiry_id').get(enquiry_id=enquiry_id),
							ec_sid = models.EnquiryComponents.objects.only('ec_sid').get(ec_sid=s.ec_sid),
							task_id = models.TaskTypes.objects.get(task_id = 'MANAPP'),
							task_assigned_to = None,
							task_assigned_date = None,
							task_completion_date = None
						)
						models.EnquiryComponentsPreviousExaminers.objects.create(
							cer_sid = models.CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
							ec_sid = models.EnquiryComponents.objects.get(ec_sid=s.ec_sid),
							exm_position = models.EnquiryComponentsHistory.objects.get(ec_sid=s.ec_sid).exm_position
						)
		#Get username to filter tasks
		username = None
		if request.user.is_authenticated:
			username =request.user
			models.TaskManager.objects.filter(enquiry_id=enquiry_id,task_id='INITCH').update(task_assigned_to=username)
			models.TaskManager.objects.filter(enquiry_id=enquiry_id,task_id='INITCH').update(task_assigned_date=timezone.now())
		#complete the task
		models.TaskManager.objects.filter(enquiry_id=enquiry_id,task_id='INITCH').update(task_completion_date=timezone.now())
	return redirect('enquiries_list')

def iec_pass_all_view(request):
	if request.method == 'POST':
		#Get scripts for this enquiry ID, this is a join from EC to ERP
		all_initch = models.TaskManager.objects.filter(task_id='INITCH',task_completion_date__isnull=True)
		for task in all_initch:
			enquiry_id = task.enquiry_id.enquiry_id
					#Get scripts for this enquiry ID, this is a join from EC to ERP
			Scripts = models.EnquiryComponents.objects.filter(erp_sid__cer_sid = enquiry_id)
			for s in Scripts:
				if '1' in s.erp_sid.service_code:
					if not models.TaskManager.objects.filter(ec_sid=s.ec_sid, task_id='CLERIC',task_completion_date = None).exists():
						models.TaskManager.objects.create(
						enquiry_id = models.CentreEnquiryRequests.objects.only('enquiry_id').get(enquiry_id=enquiry_id),
						ec_sid = models.EnquiryComponents.objects.only('ec_sid').get(ec_sid=s.ec_sid),
						task_id = models.TaskTypes.objects.get(task_id = 'CLERIC'),
						task_assigned_to = None,
						task_assigned_date = None,
						task_completion_date = None
						)
				else:
					if models.EnquiryComponentsExaminerChecks.objects.filter(ec_sid = s.ec_sid).count() > 0:
						if not models.TaskManager.objects.filter(ec_sid=s.ec_sid, task_id='PEXMCH',task_completion_date = None).exists():
							models.TaskManager.objects.create(
							enquiry_id = models.CentreEnquiryRequests.objects.only('enquiry_id').get(enquiry_id=enquiry_id),
							ec_sid = models.EnquiryComponents.objects.only('ec_sid').get(ec_sid=s.ec_sid),
							task_id = models.TaskTypes.objects.get(task_id = 'PEXMCH'),
							task_assigned_to = None,
							task_assigned_date = None,
							task_completion_date = None
							)
					else:
					#create a new task for the next step (AUTAPP)
						if not models.TaskManager.objects.filter(ec_sid=s.ec_sid, task_id='MANAPP',task_completion_date = None).exists():
							models.TaskManager.objects.create(
								enquiry_id = models.CentreEnquiryRequests.objects.only('enquiry_id').get(enquiry_id=enquiry_id),
								ec_sid = models.EnquiryComponents.objects.only('ec_sid').get(ec_sid=s.ec_sid),
								task_id = models.TaskTypes.objects.get(task_id = 'MANAPP'),
								task_assigned_to = None,
								task_assigned_date = None,
								task_completion_date = None
							)
							models.EnquiryComponentsPreviousExaminers.objects.create(
								cer_sid = models.CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
								ec_sid = models.EnquiryComponents.objects.get(ec_sid=s.ec_sid),
								exm_position = models.EnquiryComponentsHistory.objects.get(ec_sid=s.ec_sid).exm_position
							)
				#complete the task
			if request.user.is_authenticated:
				username =request.user
				models.TaskManager.objects.filter(enquiry_id=enquiry_id,task_id='INITCH').update(task_assigned_to=username)
				models.TaskManager.objects.filter(enquiry_id=enquiry_id,task_id='INITCH').update(task_assigned_date=timezone.now())
			#complete the task
			models.TaskManager.objects.filter(enquiry_id=enquiry_id,task_id='INITCH').update(task_completion_date=timezone.now())

	return redirect('enquiries_list')

def iec_fail_view(request, enquiry_id=None):
	if enquiry_id is not None and request.method == 'POST':	
		#Get scripts for this enquiry ID, this is a join from EC to ERP
		#No need for script id, BIE is handled at Enquiry Level
		if not models.TaskManager.objects.filter(enquiry_id=enquiry_id, task_id='SETBIE',task_completion_date = None).exists():
			this_task = models.TaskManager.objects.create(
				enquiry_id = models.CentreEnquiryRequests.objects.only('enquiry_id').get(enquiry_id=enquiry_id),
				ec_sid = None,
				task_id = models.TaskTypes.objects.get(task_id = 'SETBIE'),
				task_assigned_to = None,
				task_assigned_date = None,
				task_completion_date = None
			)
			this_task.refresh_from_db()
			models.SetBIEAudit.objects.create(
				rpa_task_key = models.TaskManager.objects.get(pk=this_task.pk),
				failure_reason = request.POST.get('rpa_fail')
			)
		#complete the task
		models.TaskManager.objects.filter(enquiry_id=enquiry_id,task_id='INITCH').update(task_completion_date=timezone.now())

	if request.POST.get('page_source')=='detail':
		return redirect('enquiries_detail', enquiry_id)
	else:
		return redirect('enquiries_list')

def iec_issue_view(request, enquiry_id=None):
	if enquiry_id is not None and request.method == 'POST':
		#Get scripts for this enquiry ID, this is a join from EC to ERP
		Scripts = models.EnquiryComponents.objects.filter(erp_sid__cer_sid = enquiry_id)
		for s in Scripts:
			if '1' in s.erp_sid.service_code:
				if not models.TaskManager.objects.filter(ec_sid=s.ec_sid, task_id='CLERIC',task_completion_date = None).exists():
					models.TaskManager.objects.create(
					enquiry_id = models.CentreEnquiryRequests.objects.only('enquiry_id').get(enquiry_id=enquiry_id),
					ec_sid = models.EnquiryComponents.objects.only('ec_sid').get(ec_sid=s.ec_sid),
					task_id = models.TaskTypes.objects.get(task_id = 'CLERIC'),
					task_assigned_to = None,
					task_assigned_date = None,
					task_completion_date = None
					)
			else:
				if models.EnquiryComponentsExaminerChecks.objects.filter(ec_sid = s.ec_sid).count() > 0:
					if not models.TaskManager.objects.filter(ec_sid=s.ec_sid, task_id='PEXMCH',task_completion_date = None).exists():
						models.TaskManager.objects.create(
						enquiry_id = models.CentreEnquiryRequests.objects.only('enquiry_id').get(enquiry_id=enquiry_id),
						ec_sid = models.EnquiryComponents.objects.only('ec_sid').get(ec_sid=s.ec_sid),
						task_id = models.TaskTypes.objects.get(task_id = 'PEXMCH'),
						task_assigned_to = None,
						task_assigned_date = None,
						task_completion_date = None
						)
				else:
				#create a new task for the next step (AUTAPP)
					if not models.TaskManager.objects.filter(ec_sid=s.ec_sid, task_id='MANAPP',task_completion_date = None).exists():
						models.TaskManager.objects.create(
							enquiry_id = models.CentreEnquiryRequests.objects.only('enquiry_id').get(enquiry_id=enquiry_id),
							ec_sid = models.EnquiryComponents.objects.only('ec_sid').get(ec_sid=s.ec_sid),
							task_id = models.TaskTypes.objects.get(task_id = 'MANAPP'),
							task_assigned_to = None,
							task_assigned_date = None,
							task_completion_date = None
						)
						models.EnquiryComponentsPreviousExaminers.objects.create(
							cer_sid = models.CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
							ec_sid = models.EnquiryComponents.objects.get(ec_sid=s.ec_sid),
							exm_position = models.EnquiryComponentsHistory.objects.get(ec_sid=s.ec_sid).exm_position
						)
		#Get username to filter tasks
		username = None
		if request.user.is_authenticated:
			username =request.user
			models.TaskManager.objects.filter(enquiry_id=enquiry_id,task_id='INITCH').update(task_assigned_to=username)
			models.TaskManager.objects.filter(enquiry_id=enquiry_id,task_id='INITCH').update(task_assigned_date=timezone.now())
		#complete the task
		models.TaskManager.objects.filter(enquiry_id=enquiry_id,task_id='INITCH').update(task_completion_date=timezone.now())
		if not models.SetIssueAudit.objects.filter(enquiry_id=enquiry_id).exists():
			models.SetIssueAudit.objects.create(
				enquiry_id = models.CentreEnquiryRequests.objects.only('enquiry_id').get(enquiry_id=enquiry_id),
				issue_reason = request.POST.get('rpa_fail')
			)
		#complete the task
		models.TaskManager.objects.filter(enquiry_id=enquiry_id,task_id='INITCH').update(task_completion_date=timezone.now())

		return redirect('enquiries_list')

def manapp_list_view(request):
	# grab the model rows (ordered by id), filter to required task and where not completed.
	ec_queryset = models.EnquiryComponents.objects.filter(script_tasks__task_id='MANAPP', script_tasks__task_completion_date__isnull=True).order_by('ec_sid')
	ec_queryset_paged = Paginator(ec_queryset,10,0,True)
	page_number = request.GET.get('page')
	try:
		page_obj = ec_queryset_paged.get_page(page_number)  # returns the desired page object
	except PageNotAnInteger:
		# if page_number is not an integer then assign the first page
		page_obj = ec_queryset_paged.page(1)
	except EmptyPage:
		# if page is empty then return last page
		page_obj = ec_queryset_paged.page(ec_queryset_paged.num_pages)	
	context = {"cer": page_obj,}
	return render(request, "enquiries_manual_apportionment.html", context=context)

def nrmacc_list_view(request):
	# grab the model rows (ordered by id), filter to required task and where not completed.
	ec_queryset = models.EnquiryComponents.objects.filter(script_tasks__task_id='NRMACC', script_tasks__task_completion_date__isnull=True).order_by('ec_sid')
	ec_queryset_paged = Paginator(ec_queryset,10,0,True)
	page_number = request.GET.get('page')
	try:
		page_obj = ec_queryset_paged.get_page(page_number)  # returns the desired page object
	except PageNotAnInteger:
		# if page_number is not an integer then assign the first page
		page_obj = ec_queryset_paged.page(1)
	except EmptyPage:
		# if page is empty then return last page
		page_obj = ec_queryset_paged.page(ec_queryset_paged.num_pages)	
	context = {"cer": page_obj,}
	return render(request, "enquiries_nrmacc.html", context=context)

def misvrm_list_view(request):
	# grab the model rows (ordered by id), filter to required task and where not completed.
	ec_queryset = models.EnquiryComponents.objects.filter(script_tasks__task_id='MISVRM', script_tasks__task_completion_date__isnull=True).order_by('ec_sid')
	ec_queryset_paged = Paginator(ec_queryset,10,0,True)
	page_number = request.GET.get('page')
	try:
		page_obj = ec_queryset_paged.get_page(page_number)  # returns the desired page object
	except PageNotAnInteger:
		# if page_number is not an integer then assign the first page
		page_obj = ec_queryset_paged.page(1)
	except EmptyPage:
		# if page is empty then return last page
		page_obj = ec_queryset_paged.page(ec_queryset_paged.num_pages)	
	context = {"cer": page_obj,}
	return render(request, "enquiries_misvrm.html", context=context)

def cleric_list_view(request):
	# grab the model rows (ordered by id), filter to required task and where not completed.
	ec_queryset = models.EnquiryComponents.objects.filter(script_tasks__task_id='CLERIC', script_tasks__task_completion_date__isnull=True).order_by('ec_sid')
	ec_queryset_paged = Paginator(ec_queryset,10,0,True)
	page_number = request.GET.get('page')
	try:
		page_obj = ec_queryset_paged.get_page(page_number)  # returns the desired page object
	except PageNotAnInteger:
		# if page_number is not an integer then assign the first page
		page_obj = ec_queryset_paged.page(1)
	except EmptyPage:
		# if page is empty then return last page
		page_obj = ec_queryset_paged.page(ec_queryset_paged.num_pages)	
	context = {"cer": page_obj,}
	return render(request, "enquiries_cleric.html", context=context)

def pexmch_list_view(request):
	# grab the model rows (ordered by id), filter to required task and where not completed.
	ec_queryset = models.EnquiryComponents.objects.filter(script_tasks__task_id='PEXMCH', script_tasks__task_completion_date__isnull=True).order_by('ec_sid')
	ec_queryset_paged = Paginator(ec_queryset,10,0,True)
	page_number = request.GET.get('page')
	try:
		page_obj = ec_queryset_paged.get_page(page_number)  # returns the desired page object
	except PageNotAnInteger:
		# if page_number is not an integer then assign the first page
		page_obj = ec_queryset_paged.page(1)
	except EmptyPage:
		# if page is empty then return last page
		page_obj = ec_queryset_paged.page(ec_queryset_paged.num_pages)	
	context = {"cer": page_obj,}
	return render(request, "enquiries_pexmch.html", context=context)

def esmcsv_list_view(request):
	ec_queryset = models.EsmcsvDownloads.objects.order_by('-uploaded_at')
	ec_queryset_paged = Paginator(ec_queryset,20,0,True)
	page_number = request.GET.get('page')
	try:
		page_obj = ec_queryset_paged.get_page(page_number)  # returns the desired page object
	except PageNotAnInteger:
		# if page_number is not an integer then assign the first page
		page_obj = ec_queryset_paged.page(1)
	except EmptyPage:
		# if page is empty then return last page
		page_obj = ec_queryset_paged.page(ec_queryset_paged.num_pages)	
	context = {"cer": page_obj,}
	return render(request, "enquiries_esmcsv.html", context=context)

def esmcsv_create_view(request):
	ec_queryset = models.TaskManager.objects.filter(task_id='ESMCSV', task_completion_date__isnull=True, ec_sid__script_id__eb_sid__eb_sid__isnull=False)
	if ec_queryset.count() > 0:
		file_timestamp = timezone.now().strftime("%m_%d_%Y_%H_%M_%S") + ".csv"
		file_location = os.path.join(settings.MEDIA_ROOT, "downloads", file_timestamp).replace('\\', '/')
		print(file_location)
		username = None
		if request.user.is_authenticated:
			username =request.user		
		with open(file_location, 'w', newline='') as file:
			file.truncate()
			writer = csv.writer(file)
			for s in ec_queryset:
				syllcomp = s.ec_sid.eps_ass_code + "/" + s.ec_sid.eps_com_id
				batch = models.EnquiryComponentElements.objects.get(ec_sid = s.ec_sid).eb_sid.eb_sid
				session = s.ec_sid.eps_ses_name
				candidate = s.ec_sid.erp_sid.eps_cand_id
				centre = s.ec_sid.erp_sid.eps_centre_id
				examiner_name = models.ScriptApportionment.objects.get(ec_sid = s.ec_sid).enpe_sid.per_sid.exm_forename + " " + models.ScriptApportionment.objects.get(ec_sid = s.ec_sid).enpe_sid.per_sid.exm_surname
				examiner_pos = models.EnquiryPersonnelDetails.objects.filter(enpe_sid = models.ScriptApportionment.objects.get(ec_sid = s.ec_sid).enpe_sid).first().exm_examiner_no
				creditor_number = models.ScriptApportionment.objects.get(ec_sid = s.ec_sid).enpe_sid.per_sid.exm_creditor_no

				writer.writerow([syllcomp,batch,session,candidate,centre,examiner_name, examiner_pos, creditor_number, ""])
				models.TaskManager.objects.filter(ec_sid=s.ec_sid,task_id='ESMCSV').update(task_completion_date=timezone.now())
				models.TaskManager.objects.filter(ec_sid=s.ec_sid,task_id='ESMCSV').update(task_assigned_date=timezone.now())
				models.TaskManager.objects.filter(ec_sid=s.ec_sid,task_id='ESMCSV').update(task_assigned_to=username)

		models.EsmcsvDownloads.objects.create(
			document = file_location,
			file_name = file_timestamp,
			download_count = 0,
			archive_count = 0
			)
		
			#Get username to filter tasks

		


	return redirect('esmcsv_list')

def esmcsv_download_view(request, download_id=None):
	# 
	document = models.EsmcsvDownloads.objects.get(pk=download_id).document
	downloads = int(models.EsmcsvDownloads.objects.get(pk=download_id).download_count) + 1
	models.EsmcsvDownloads.objects.filter(pk=download_id).update(download_count = str(downloads))

	return FileResponse(document, as_attachment=True)


def exmsla_list_view(request):
	# grab the model rows (ordered by id), filter to required task and where not completed.
	ec_queryset = models.EnquiryComponents.objects.filter(script_tasks__task_id='EXMSLA', script_tasks__task_completion_date__isnull=True).order_by('ec_sid')
	ec_queryset_paged = Paginator(ec_queryset,10,0,True)
	page_number = request.GET.get('page')
	try:
		page_obj = ec_queryset_paged.get_page(page_number)  # returns the desired page object
	except PageNotAnInteger:
		# if page_number is not an integer then assign the first page
		page_obj = ec_queryset_paged.page(1)
	except EmptyPage:
		# if page is empty then return last page
		page_obj = ec_queryset_paged.page(ec_queryset_paged.num_pages)	
	context = {"cer": page_obj,}
	return render(request, "enquiries_exmsla.html", context=context)

def remapp_list_view(request):
	# grab the model rows (ordered by id), filter to required task and where not completed.
	ec_queryset = models.EnquiryComponents.objects.filter(script_tasks__task_id='REMAPP', script_tasks__task_completion_date__isnull=True).order_by('ec_sid')
	ec_queryset_paged = Paginator(ec_queryset,10,0,True)
	page_number = request.GET.get('page')
	try:
		page_obj = ec_queryset_paged.get_page(page_number)  # returns the desired page object
	except PageNotAnInteger:
		# if page_number is not an integer then assign the first page
		page_obj = ec_queryset_paged.page(1)
	except EmptyPage:
		# if page is empty then return last page
		page_obj = ec_queryset_paged.page(ec_queryset_paged.num_pages)	
	context = {"cer": page_obj,}
	return render(request, "enquiries_remapp.html", context=context)

def remapf_list_view(request):
	# grab the model rows (ordered by id), filter to required task and where not completed.
	ec_queryset = models.EnquiryComponents.objects.filter(script_tasks__task_id='REMAPF', script_tasks__task_completion_date__isnull=True).order_by('ec_sid')
	ec_queryset_paged = Paginator(ec_queryset,10,0,True)
	page_number = request.GET.get('page')
	try:
		page_obj = ec_queryset_paged.get_page(page_number)  # returns the desired page object
	except PageNotAnInteger:
		# if page_number is not an integer then assign the first page
		page_obj = ec_queryset_paged.page(1)
	except EmptyPage:
		# if page is empty then return last page
		page_obj = ec_queryset_paged.page(ec_queryset_paged.num_pages)	
	context = {"cer": page_obj,}
	return render(request, "enquiries_remapf.html", context=context)


def grdrel_create_view(request):
	task_queryset = models.TaskManager.objects.filter(task_id='GRDREL', task_completion_date__isnull=True)
	if task_queryset.count() > 0:
		for t in task_queryset:
			enquiry_id = t.enquiry_id.enquiry_id
			if not models.TaskManager.objects.filter(enquiry_id=enquiry_id, task_id='GRDMAT',task_completion_date = None).exists():
				models.TaskManager.objects.create(
					enquiry_id = models.CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
					ec_sid = None,
					task_id = models.TaskTypes.objects.get(task_id = 'GRDMAT'),
					task_assigned_to = User.objects.get(username='NovaServer'),
					task_assigned_date = timezone.now(),
					task_completion_date = None
				)

			#Get username to filter tasks
			username = None
			if request.user.is_authenticated:
				username =request.user
			
			models.TaskManager.objects.filter(enquiry_id=t.enquiry_id.enquiry_id,task_id='GRDREL').update(task_completion_date=timezone.now())
			models.TaskManager.objects.filter(enquiry_id=t.enquiry_id.enquiry_id,task_id='GRDREL').update(task_assigned_date=timezone.now())
			models.TaskManager.objects.filter(enquiry_id=t.enquiry_id.enquiry_id,task_id='GRDREL').update(task_assigned_to=username)

	return redirect('enquiries_home')

def negcon_list_view(request):
	# grab the model rows (ordered by id), filter to required task and where not completed.
	ec_queryset = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='NEGCON', enquiry_tasks__task_completion_date__isnull=True).order_by('enquiry_id')
	ec_queryset_paged = Paginator(ec_queryset,10,0,True)
	page_number = request.GET.get('page')
	try:
		page_obj = ec_queryset_paged.get_page(page_number)  # returns the desired page object
	except PageNotAnInteger:
		# if page_number is not an integer then assign the first page
		page_obj = ec_queryset_paged.page(1)
	except EmptyPage:
		# if page is empty then return last page
		page_obj = ec_queryset_paged.page(ec_queryset_paged.num_pages)	
	context = {"cer": page_obj,}
	return render(request, "enquiries_negcon.html", context=context)

def pdacon_list_view(request):
	# grab the model rows (ordered by id), filter to required task and where not completed.
	ec_queryset = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='PDACON', enquiry_tasks__task_completion_date__isnull=True).order_by('enquiry_id')
	ec_queryset_paged = Paginator(ec_queryset,10,0,True)
	page_number = request.GET.get('page')
	try:
		page_obj = ec_queryset_paged.get_page(page_number)  # returns the desired page object
	except PageNotAnInteger:
		# if page_number is not an integer then assign the first page
		page_obj = ec_queryset_paged.page(1)
	except EmptyPage:
		# if page is empty then return last page
		page_obj = ec_queryset_paged.page(ec_queryset_paged.num_pages)	
	context = {"cer": page_obj,}
	return render(request, "enquiries_pdacon.html", context=context)

def peacon_list_view(request):
	# grab the model rows (ordered by id), filter to required task and where not completed.
	ec_queryset = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='PEACON', enquiry_tasks__task_completion_date__isnull=True).order_by('enquiry_id')
	ec_queryset_paged = Paginator(ec_queryset,10,0,True)
	page_number = request.GET.get('page')
	try:
		page_obj = ec_queryset_paged.get_page(page_number)  # returns the desired page object
	except PageNotAnInteger:
		# if page_number is not an integer then assign the first page
		page_obj = ec_queryset_paged.page(1)
	except EmptyPage:
		# if page is empty then return last page
		page_obj = ec_queryset_paged.page(ec_queryset_paged.num_pages)	
	context = {"cer": page_obj,}
	return render(request, "enquiries_peacon.html", context=context)

def grdchg_list_view(request):
	# grab the model rows (ordered by id), filter to required task and where not completed.
	ec_queryset = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='GRDCHG', enquiry_tasks__task_completion_date__isnull=True).order_by('enquiry_id')
	ec_queryset_paged = Paginator(ec_queryset,10,0,True)
	page_number = request.GET.get('page')
	try:
		page_obj = ec_queryset_paged.get_page(page_number)  # returns the desired page object
	except PageNotAnInteger:
		# if page_number is not an integer then assign the first page
		page_obj = ec_queryset_paged.page(1)
	except EmptyPage:
		# if page is empty then return last page
		page_obj = ec_queryset_paged.page(ec_queryset_paged.num_pages)	
	context = {"cer": page_obj,}
	return render(request, "enquiries_grdchg.html", context=context)

def grdrej_list_view(request):
	# grab the model rows (ordered by id), filter to required task and where not completed.
	ec_queryset = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='GRDREJ', enquiry_tasks__task_completion_date__isnull=True).order_by('enquiry_id')
	ec_queryset_paged = Paginator(ec_queryset,10,0,True)
	page_number = request.GET.get('page')
	try:
		page_obj = ec_queryset_paged.get_page(page_number)  # returns the desired page object
	except PageNotAnInteger:
		# if page_number is not an integer then assign the first page
		page_obj = ec_queryset_paged.page(1)
	except EmptyPage:
		# if page is empty then return last page
		page_obj = ec_queryset_paged.page(ec_queryset_paged.num_pages)	
	context = {"cer": page_obj,}
	return render(request, "enquiries_grdrej.html", context=context)

def mrkamd_list_view(request):
	# grab the model rows (ordered by id), filter to required task and where not completed.
	ec_queryset = models.CentreEnquiryRequests.objects.filter(enquiry_tasks__task_id='MRKAMD', enquiry_tasks__task_completion_date__isnull=True).order_by('enquiry_id')
	ec_queryset_paged = Paginator(ec_queryset,10,0,True)
	page_number = request.GET.get('page')
	try:
		page_obj = ec_queryset_paged.get_page(page_number)  # returns the desired page object
	except PageNotAnInteger:
		# if page_number is not an integer then assign the first page
		page_obj = ec_queryset_paged.page(1)
	except EmptyPage:
		# if page is empty then return last page
		page_obj = ec_queryset_paged.page(ec_queryset_paged.num_pages)	
	context = {"cer": page_obj,}
	return render(request, "enquiries_mrkamd.html", context=context)

def enquiries_rpa_apportion_view(request):
	# grab the model rows (ordered by id), filter to required task and where not completed.
	ec_queryset = models.EnquiryComponents.objects.filter(script_tasks__task_id='BOTAPP', script_tasks__task_completion_date__isnull=True).order_by('ec_sid')
	ec_queryset_paged = Paginator(ec_queryset,10,0,True)
	page_number = request.GET.get('page')
	try:
		page_obj = ec_queryset_paged.get_page(page_number)  # returns the desired page object
	except PageNotAnInteger:
		# if page_number is not an integer then assign the first page
		page_obj = ec_queryset_paged.page(1)
	except EmptyPage:
		# if page is empty then return last page
		page_obj = ec_queryset_paged.page(ec_queryset_paged.num_pages)	
	context = {"ec_queryset": page_obj,}
	return render(request, 'rpa_apportionment.html', context=context)

def rpa_apportion_pass_view(request, script_id=None):
	if script_id is not None and request.method == 'POST':
		#Mark the task with this script ID for BOTAPP as complete
		models.TaskManager.objects.filter(ec_sid=script_id,task_id='BOTAPP').update(task_completion_date=timezone.now())
	return redirect('rpa_apportionment')

def rpa_apportion_fail_view(request, script_id=None):
	if script_id is not None and request.method == 'POST':	
		#Get enquiry for this script ID
		#create a new task for the next step (BOTAPF)
		if not models.TaskManager.objects.filter(ec_sid=models.EnquiryComponents.objects.only('ec_sid').get(ec_sid=script_id), task_id='BOTAPF',task_completion_date = None).exists():
			this_task = models.TaskManager.objects.create(
				enquiry_id = models.CentreEnquiryRequests.objects.get(enquiries__enquiry_parts__ec_sid=script_id),
				ec_sid = models.EnquiryComponents.objects.get(ec_sid=script_id),
				task_id = models.TaskTypes.objects.get(task_id = 'BOTAPF'),
				task_assigned_to = None,
				task_assigned_date = None,
				task_completion_date = None
			)
			this_task.refresh_from_db()
			print(this_task.pk)
			models.RpaFailureAudit.objects.create(
				rpa_task_key = models.TaskManager.objects.get(pk=this_task.pk),
				failure_reason = request.POST.get('rpa_fail')
			)
		#complete the task
		models.TaskManager.objects.filter(ec_sid=script_id,task_id='BOTAPP').update(task_completion_date=timezone.now())
		return redirect('rpa_apportionment')

def enquiries_rpa_apportion_failure_view(request):
	ec_queryset = models.EnquiryComponents.objects.filter(script_tasks__task_id='BOTAPF', script_tasks__task_completion_date__isnull=True).order_by('ec_sid')
	ec_queryset_paged = Paginator(ec_queryset,10,0,True)
	page_number = request.GET.get('page')
	try:
		page_obj = ec_queryset_paged.get_page(page_number)  # returns the desired page object
	except PageNotAnInteger:
		# if page_number is not an integer then assign the first page
		page_obj = ec_queryset_paged.page(1)
	except EmptyPage:
		# if page is empty then return last page
		page_obj = ec_queryset_paged.page(ec_queryset_paged.num_pages)	
	context = {"cer": page_obj,}
	return render(request, "rpa_apportionment_failure.html", context=context)


def enquiries_rpa_marks_keying_view(request):
	# grab the model rows (ordered by id), filter to required task and where not completed.
	ec_queryset = models.EnquiryComponents.objects.filter(script_tasks__task_id='BOTMAR', script_tasks__task_completion_date__isnull=True).order_by('ec_sid')
	ec_queryset_paged = Paginator(ec_queryset,10,0,True)
	page_number = request.GET.get('page')
	try:
		page_obj = ec_queryset_paged.get_page(page_number)  # returns the desired page object
	except PageNotAnInteger:
		# if page_number is not an integer then assign the first page
		page_obj = ec_queryset_paged.page(1)
	except EmptyPage:
		# if page is empty then return last page
		page_obj = ec_queryset_paged.page(ec_queryset_paged.num_pages)	
	context = {"ec_queryset": page_obj,}
	return render(request, 'rpa_marks_keying.html', context=context)

def rpa_marks_keying_pass_view(request, script_id=None):
	if script_id is not None and request.method == 'POST':
		enquiry_id = models.TaskManager.objects.filter(ec_sid=script_id,task_id='BOTMAR').first().enquiry_id.enquiry_id
		#check if this enquiry already exists at GDWAIT
		gdwait_task = 0
		gdwait_task = models.TaskManager.objects.filter(enquiry_id=enquiry_id,task_id='GDWAIT').count()
		if gdwait_task == 0:
			if not models.TaskManager.objects.filter(enquiry_id=enquiry_id, task_id='GDWAIT',task_completion_date = None).exists():
				models.TaskManager.objects.create(
					enquiry_id = models.CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
					ec_sid = None,
					task_id = models.TaskTypes.objects.get(task_id = 'GDWAIT'),
					task_assigned_to = User.objects.get(username='NovaServer'),
					task_assigned_date = timezone.now(),
					task_completion_date = None
				)
		#Mark the task with this script ID for BOTMAR as complete
		models.TaskManager.objects.filter(ec_sid=script_id,task_id='BOTMAR').update(task_completion_date=timezone.now())
		models.ScriptApportionment.objects.filter(ec_sid=script_id,script_marked=0,apportionment_invalidated=0).update(script_mark_entered=0)
	return redirect('rpa_marks_keying')

def rpa_marks_keying_fail_view(request, script_id=None):
	if script_id is not None and request.method == 'POST':	
		enquiry_id = models.TaskManager.objects.filter(ec_sid=script_id,task_id='BOTMAR').first().enquiry_id.enquiry_id
		#create a new task for the next step (BOTMAF)
		if not models.TaskManager.objects.filter(enquiry_id=enquiry_id, task_id='BOTMAF',task_completion_date = None).exists():
			this_task = models.TaskManager.objects.create(
				enquiry_id = models.CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id),
				ec_sid = models.EnquiryComponents.objects.get(ec_sid=script_id),
				task_id = models.TaskTypes.objects.get(task_id = 'BOTMAF'),
				task_assigned_to = None,
				task_assigned_date = None,
				task_completion_date = None
			)
			this_task.refresh_from_db()
			models.RpaFailureAudit.objects.create(
				rpa_task_key = models.TaskManager.objects.get(pk=this_task.pk),
				failure_reason = request.POST.get('rpa_fail')
			)
		#complete the task
		models.TaskManager.objects.filter(ec_sid=script_id,task_id='BOTMAR').update(task_completion_date=timezone.now())
		return redirect('rpa_marks_keying')

def enquiries_rpa_marks_keying_failure_view(request):
	# grab the model rows (ordered by id), filter to required task and where not completed.
	ec_queryset = models.EnquiryComponents.objects.filter(script_tasks__task_id='BOTMAF', script_tasks__task_completion_date__isnull=True).order_by('ec_sid')
	ec_queryset_paged = Paginator(ec_queryset,10,0,True)
	page_number = request.GET.get('page')
	try:
		page_obj = ec_queryset_paged.get_page(page_number)  # returns the desired page object
	except PageNotAnInteger:
		# if page_number is not an integer then assign the first page
		page_obj = ec_queryset_paged.page(1)
	except EmptyPage:
		# if page is empty then return last page
		page_obj = ec_queryset_paged.page(ec_queryset_paged.num_pages)	
	context = {"cer": page_obj,}
	return render(request, "rpa_marks_keying_failure.html", context=context)


#TO DO: Pause Enquiry
def pause_enquiry(request, enquiry_id=None):
	if enquiry_id is not None and request.method == 'POST':	
		enquiry_obj = models.CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id)
		#enquiry_obj.initial_check_complete = True
		#enquiry_obj.save()
	return redirect('enquiries_detail', enquiry_id)

#TO DO: Prioritise Enquiry
def prioritise_enquiry(request, enquiry_id=None):
	if enquiry_id is not None and request.method == 'POST':	
		enquiry_obj = models.CentreEnquiryRequests.objects.get(enquiry_id=enquiry_id)
		#enquiry_obj.initial_check_complete = True
		#enquiry_obj.save()
	return redirect('enquiries_detail', enquiry_id)

def examiner_list_view(request):
	search_q = ""
	if request.GET.get('search_query') is not None:
		search_q = request.GET.get('search_query')
	split_search_q_1 = "None"
	split_search_q_2 = "None"
	if search_q.find("/") > -1:
		split_search_q_1 = search_q.split("/")[0]
		split_search_q_2 = search_q.split("/")[1]
	ep_queryset = models.UniqueCreditor.objects.filter(Q(exm_creditor_no__icontains = search_q) | Q(exm_surname__icontains = search_q) | Q(creditors__exm_per_details__ass_code__icontains = split_search_q_1) & Q(creditors__exm_per_details__com_id__icontains = split_search_q_2)).order_by('exm_creditor_no').distinct()

	ep_queryset_paged = Paginator(ep_queryset,10,0,True)
	page_number = request.GET.get('page')
	try:
		page_obj = ep_queryset_paged.get_page(page_number)  # returns the desired page object
	except PageNotAnInteger:
		# if page_number is not an integer then assign the first page
		page_obj = ep_queryset_paged.page(1)
	except EmptyPage:
		# if page is empty then return last page
		page_obj = ep_queryset_paged.page(ep_queryset_paged.num_pages)	
	context = {"ep": page_obj, "sq":search_q, }
	return render(request, "enquiries_examiner_list.html", context=context)

def examiner_detail(request, per_sid=None):
	exm_queryset = None
	if per_sid is not None:	
		uc_queryset = models.UniqueCreditor.objects.get(per_sid=per_sid)
		exm_queryset = models.EnquiryPersonnel.objects.filter(per_sid=per_sid)
		exm_queryset2 = models.EnquiryPersonnelDetails.objects.filter(enpe_sid__per_sid=per_sid)
		#examiner email override check
		try:
			email_new = models.ExaminerEmailOverride.objects.get(creditor__per_sid = per_sid).examiner_email_manual
		except:
			email_new = models.UniqueCreditor.objects.get(per_sid=per_sid).exm_email


	context = {"uc": uc_queryset, "exm": exm_queryset, "exm2": exm_queryset2, "exm_email": email_new}
	return render(request, 'enquiries_examiner_detail.html', context=context)

def examiner_scripts_view(request, per_sid=None):
	enpe_queryset = models.EnquiryPersonnel.objects.filter(per_sid=per_sid).first()
	# grab the model rows (ordered by id), filter to required task and where not completed.
	ec_queryset = models.ScriptApportionment.objects.filter(enpe_sid=enpe_queryset.enpe_sid,apportionment_invalidated=0).order_by('-script_marked','-script_mark_entered','ec_sid')
	ec_queryset_paged = Paginator(ec_queryset,10,0,True)
	page_number = request.GET.get('page')
	try:
		page_obj = ec_queryset_paged.get_page(page_number)  # returns the desired page object
	except PageNotAnInteger:
		# if page_number is not an integer then assign the first page
		page_obj = ec_queryset_paged.page(1)
	except EmptyPage:
		# if page is empty then return last page
		page_obj = ec_queryset_paged.page(ec_queryset_paged.num_pages)	
	context = {"cer": page_obj,"enpe": enpe_queryset}
	return render(request, "enquiries_examiner_scripts.html", context=context)

def examiner_availability_view(request, per_sid=None):
	uc_queryset = models.UniqueCreditor.objects.get(per_sid=per_sid)
	context = {"enpe": uc_queryset,}
	return render(request, 'enquiries_examiner_availability.html', context=context)

def examiner_availability_edit_view(request, per_sid=None):
	print(per_sid)
	print(request.POST.get('start'))
	if per_sid is not None and request.method == 'POST':
		exm = models.UniqueCreditor.objects.get(per_sid=per_sid)
		avail = models.ExaminerAvailability(
			#ea_sid = models.EnquiryPersonnel.objects.only('enpe_sid').get(enpe_sid=enpe_sid),
			unavailability_start_date = request.POST.get('start'),
			unavailability_end_date = request.POST.get('end'),
			unavailable_2_flag = request.POST.get('esstwo'),
			unavailable_5_flag = request.POST.get('essfive'),
			unavailable_9_flag = request.POST.get('essnine'),
		)
		avail.save()
		avail.creditor.add(exm)
	return redirect('examiner_detail', per_sid)

def examiner_availability_delete(request, note_id=None):
	if note_id is not None:
		per_sid = models.UniqueCreditor.objects.get(exm_availability__pk = note_id).per_sid
		models.ExaminerAvailability.objects.get(id=note_id).delete()
	return redirect('examiner_detail', per_sid)

def examiner_notes_view(request, per_sid=None):
	uc_queryset = models.UniqueCreditor.objects.get(per_sid=per_sid)
	context = {"enpe": uc_queryset,}
	return render(request, 'enquiries_examiner_notes.html', context=context)

def examiner_notes_edit_view(request, per_sid=None):
		#Get username to filter tasks
	username = None
	if request.user.is_authenticated:
		username = request.user

	if per_sid is not None and request.method == 'POST':
		exm = models.UniqueCreditor.objects.get(per_sid=per_sid)
		note_entry = models.ExaminerNotes(
			examiner_notes = request.POST.get('exm_note'),
			note_owner = username,
		)
		note_entry.save()
		note_entry.creditor.add(exm)
	return redirect('examiner_detail', per_sid)

def examiner_notes_delete(request, note_id=None):
	if note_id is not None:
		per_sid = models.UniqueCreditor.objects.get(exm_notes__pk = note_id).per_sid
		models.ExaminerNotes.objects.get(id=note_id).delete()
	return redirect('examiner_detail', per_sid)

def examiner_conflicts_view(request, per_sid=None):
	uc_queryset = models.UniqueCreditor.objects.get(per_sid=per_sid)
	if models.ExaminerConflicts.objects.filter(creditor=uc_queryset).exists():
		current_conflict = models.ExaminerConflicts.objects.get(creditor=uc_queryset)
	else:
		current_conflict = None
	context = {"enpe": uc_queryset, "current_conflict":current_conflict}
	return render(request, 'enquiries_examiner_conflicts.html', context=context)

def examiner_conflicts_edit_view(request, per_sid=None):
	#Get username
	username = None
	if request.user.is_authenticated:
		username = request.user

	if per_sid is not None and request.method == 'POST':
		exm = models.UniqueCreditor.objects.get(per_sid=per_sid)
		#detect if note exists or not
		try:
			existing_note = models.ExaminerConflicts.objects.get(creditor__per_sid = per_sid).pk
		except:
			existing_note = None
		#if note does not exist, create it, else update it
		if existing_note is None:
			conflict_entry = models.ExaminerConflicts(
				examiner_conflicts = request.POST.get('exm_conflicts'),
				note_owner = username,
			)
			conflict_entry.save()
			conflict_entry.creditor.add(exm)
		else:
			models.ExaminerConflicts.objects.filter(id=existing_note).update(examiner_conflicts=request.POST.get('exm_conflicts'))
	return redirect('examiner_detail', per_sid)

def examiner_conflicts_delete(request, note_id=None):
	if note_id is not None:
		per_sid = models.UniqueCreditor.objects.get(exm_conflicts__pk = note_id).per_sid
		models.ExaminerConflicts.objects.get(id=note_id).delete()
	return redirect('examiner_detail', per_sid)

def examiner_email_view(request, per_sid=None):
	uc_queryset = models.UniqueCreditor.objects.get(per_sid=per_sid)
	context = {"enpe": uc_queryset,}
	return render(request, 'enquiries_examiner_email.html', context=context)

def examiner_email_edit_view(request, per_sid=None):
	#Get username
	username = None
	if request.user.is_authenticated:
		username = request.user
	print(username)

	if per_sid is not None and request.method == 'POST':
		exm = models.UniqueCreditor.objects.get(per_sid=per_sid)
		#detect if note exists or not
		try:
			existing_note = models.ExaminerEmailOverride.objects.get(creditor__per_sid = per_sid).pk
		except:
			existing_note = None
		#if note does not exist, create it, else update it
		print(existing_note)
		if existing_note is None:
			conflict_entry = models.ExaminerEmailOverride(
				examiner_email_manual = request.POST.get('exm_new_email'),
			)
			conflict_entry.save()
			conflict_entry.creditor.add(exm)
		else:
			models.ExaminerEmailOverride.objects.filter(id=existing_note).update(examiner_email_manual=request.POST.get('exm_new_email'))
	return redirect('examiner_detail', per_sid)

def user_panel_view(request):
	# grab the model rows (ordered by id), filter to required task and where not completed.
	queryset = models.User.objects.filter(assigned_tasks__task_completion_date__isnull=True).exclude(user_primary__primary_team__team_name='Server').annotate(task_count=Count("assigned_tasks",distinct=True)).order_by('username','user_primary__primary_team__team_name')
	teams = models.TaskTeams.objects.all().order_by('id')
	context = {"users": queryset, "teams":teams}
	return render(request, "enquiries_task_user.html", context=context)

def create_user_view(request):
	username = request.POST.get('username')
	password = request.POST.get('password')
	email = request.POST.get('email')
	pteam = request.POST.get('pteam')
	access = request.POST.get('access')

	new_user = User.objects.create_user(username=username,
							email=email,
							password=password)
	
	models.TaskUserPrimary.objects.create(
		task_user = new_user,
		primary_team = models.TaskTeams.objects.get(team_name=pteam),
		primary_status = access
	)

	return redirect("user_panel")

def update_user_view(request):
	username = request.POST.get('username')
	pteam = request.POST.get('pteam')
	access = request.POST.get('access')

	this_user = User.objects.get(username=username)
	
	models.TaskUserPrimary.objects.filter(task_user = this_user).update(
		primary_team = models.TaskTeams.objects.get(team_name=pteam),
		primary_status = access
	)

	if models.TaskUserSecondary.objects.filter(task_user=this_user,secondary_team=models.TaskTeams.objects.get(team_name=pteam)).exists():
		models.TaskUserSecondary.objects.filter(task_user=this_user,
		secondary_team=models.TaskTeams.objects.get(team_name=pteam)).delete()
	

	return redirect("edit_user", this_user.pk)

def user_remove_tasks_view(request):
	username = request.POST.get('username')
	# grab the model rows (ordered by id), filter to required task and where not completed.
	models.TaskManager.objects.filter(task_assigned_to=models.User.objects.get(username=username)).update(task_assigned_to=None, task_assigned_date=None)
	

	return redirect("user_panel")

def edit_user_view(request, userid=None):
	teams = models.TaskTeams.objects.all().order_by('team_name')
	user = User.objects.get(id=userid)

	team_list = []
	for team in models.TaskUserSecondary.objects.filter(task_user=user):
		team_list.append(team.secondary_team.team_name)

	primary_team = models.TaskUserPrimary.objects.get(task_user=user).primary_team.team_name

	context = {"teams":teams, "user":user, "team_list":team_list, "primary_team":primary_team}
	return render(request, "enquiries_task_user_detail.html", context=context) 

def user_change_secondary(request):
	userid = request.POST.get('userid')
	sec_team = request.POST.get('sec_team')
	type = request.POST.get('type')

	if type == 'enroll':
		models.TaskUserSecondary.objects.create(
			task_user = User.objects.get(id=userid),
			secondary_team = models.TaskTeams.objects.get(team_name=sec_team)
		)
	else:
		models.TaskUserSecondary.objects.filter(
			task_user=User.objects.get(id=userid),
			secondary_team = models.TaskTeams.objects.get(team_name=sec_team)
		).delete()


	return redirect('edit_user', userid)