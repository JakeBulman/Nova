from . import models
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
import pyodbc
import pandas as pd
from openpyxl import load_workbook
from django.db.models import Sum, Count, Q
from django.utils import timezone
from django.apps import apps

PageNotAnInteger = None
EmptyPage = None

# Create your views here.
@login_required
def datareporting_home_view(request):
	num_queued = Count("task_queue", filter=Q(task_queue__task_queued='1'))
	num_running = Count("task_queue", filter=Q(task_queue__task_running='1'))
	reports_queryset = models.Reports.objects.all().annotate(num_queued=num_queued, num_running=num_running).order_by('id')

    # Get column names (I think it will be better to display this information in a different way):
	for report in reports_queryset:
		ModelClass = apps.get_model('datareporting', report.report_name)
		report.columns = [field.name for field in ModelClass._meta.fields]

	context = {
		'reports_queryset': reports_queryset,
		}
	return render(request, "datareporting/datareporting_home.html", context=context)

def run_data_load_view(request, report_id):
	#Get session ID from POST form
	parameter = request.POST.get('parameter')
	models.Reports.objects.filter(id=report_id).update(series_parameter = parameter)

	#Check if task exists in queue, and if not, create it
	if not models.ManualTaskQueue.objects.filter(report_name=report_id, task_queued=1).exists():
		models.ManualTaskQueue.objects.create(
		report_name = models.Reports.objects.get(id=report_id),
		)
		models.Reports.objects.filter(id=report_id).update(last_triggered = timezone.now())
	return redirect('datareporting_home')

def report_update_status(request, report_id):
	toggle_status = models.Reports.objects.get(id=report_id).active_refresh
	if toggle_status == True:
		toggle_status = False
	else:
		toggle_status = True
	models.Reports.objects.filter(id=report_id).update(active_refresh = toggle_status)
	return redirect('datareporting_home')