from . import models
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
import pyodbc
import pandas as pd
from openpyxl import load_workbook
from django.db.models import Sum, Count, Q
from django.utils import timezone

PageNotAnInteger = None
EmptyPage = None

# Create your views here.
@login_required
def datareporting_home_view(request):
	num_queued = Count("task_queue", filter=Q(task_queue__task_queued='1'))
	num_running = Count("task_queue", filter=Q(task_queue__task_running='1'))
	reports_queryset = models.Reports.objects.all().annotate(num_queued=num_queued,num_running=num_running)
	context = {'reports_queryset':reports_queryset}
	return render(request, "datareporting/datareporting_home.html", context=context)

def run_data_load_view(request, report_id):
	#Get session ID from POST form
	ses_sid = request.POST.get('ses_sid')
	models.Reports.objects.filter(id=report_id).update(ses_sid = ses_sid)

	#Check if task exists in queue, and if not, create it
	if not models.ManualTaskQueue.objects.filter(report_name=report_id, task_queued=1).exists():
		models.ManualTaskQueue.objects.create(
		report_name = models.Reports.objects.get(id=report_id),
		)
		models.Reports.objects.filter(id=report_id).update(last_triggered = timezone.now())
	return redirect('datareporting_home')
		