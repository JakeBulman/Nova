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
from django.contrib import messages

PageNotAnInteger = None
EmptyPage = None

# Create your views here.
@login_required
def datareporting_home_view(request):
	return render(request, "datareporting/datareporting_home.html")

def reports_view(request):
	# Fetch all instances of the Reports model
	reports_queryset = models.Reports.objects.all().order_by('id')

	# Pass the queryset to the template context
	context = {
	'reports_queryset': reports_queryset,
	}
	return render(request, "datareporting/datareporting_reports.html", context=context)

def datasets_view(request):
	num_queued = Count("task_queue", filter=Q(task_queue__task_queued='1'))
	num_running = Count("task_queue", filter=Q(task_queue__task_running='1'))
	datasets_queryset = models.Datasets.objects.all().annotate(num_queued=num_queued, num_running=num_running).order_by('id')

    # Get column names (I think it will be better to display this information in a different way):
	for dataset in datasets_queryset:
		ModelClass = apps.get_model('datareporting', dataset.dataset_name)
		dataset.columns = [field.name for field in ModelClass._meta.fields]

	context = {
		'datasets_queryset': datasets_queryset,
		}
	return render(request, "datareporting/datareporting_datasets.html", context=context)

def run_data_load_view(request, dataset_id):
	#Get session ID from POST form
	parameter = request.POST.get('parameter')
	models.Datasets.objects.filter(id=dataset_id).update(parameter = parameter)

	#Check if task exists in queue, and if not, create it
	if not models.ManualTaskQueue.objects.filter(dataset=dataset_id, task_queued=1).exists():
		models.ManualTaskQueue.objects.create(
		dataset = models.Datasets.objects.get(id=dataset_id),
		)
		models.Datasets.objects.filter(id=dataset_id).update(last_triggered = timezone.now())
	return redirect('datareporting_home')

def dataset_update_status(request, dataset_id):
	toggle_status = models.Datasets.objects.get(id=dataset_id).active_refresh
	if toggle_status == True:
		toggle_status = False
	else:
		toggle_status = True
	models.Datasets.objects.filter(id=dataset_id).update(active_refresh = toggle_status)

def new_dataset(request):
	return render(request, "datareporting/datareporting_new_dataset.html")

def add_dataset(request):
	dataset_name = request.POST.get('datasetName')
	parameter_name = request.POST.get('parameterName')

	try:
		model = apps.get_model('datareporting', dataset_name)
		if model:			
			if not models.Datasets.objects.filter(dataset_name=dataset_name).exists():
				models.Datasets.objects.create(dataset_name = dataset_name, parameter_name = parameter_name)
			else:
				messages.error(request, f"A dataset with the name '{dataset_name}' already exists.")
				return redirect('new_dataset')
	except LookupError:
		messages.error(request, f"A model with the name '{dataset_name}' does not exists.")
		return redirect('new_dataset')
	
	return redirect('datareporting_home')

def update_report_active_status(request, report_id):
	toggle_status = models.Reports.objects.get(id=report_id).active
	if toggle_status == True:
		toggle_status = False
	else:
		toggle_status = True
	models.Reports.objects.filter(id=report_id).update(active = toggle_status)

def report_datasets(request, id):
	report_info = models.Reports.objects.get(id=id)
	report_datasets_queryset = models.Report_Datasets.objects.filter(report=id).all().order_by('dataset')

	context = {
	'report_info': report_info,
	'report_datasets_queryset': report_datasets_queryset,
	}
	return render(request, "datareporting/datareporting_report_datasets.html", context=context)

def new_report(request):
	datasets_queryset = models.Datasets.objects.all().order_by('datasets')

	context = {
	'datasets_queryset': datasets_queryset,
	}
	return render(request, "datareporting/datareporting_new_report.html", context=context)

def add_report(request):
	if request.method == 'POST':
		new_report_name = request.POST.get('newReportName')
		selected_datasets_ids = request.POST.getlist('selected_dataset')
		print(selected_datasets_ids)
		selected_datasets_parameters = request.POST.getlist('dataset_parameter')
		print(selected_datasets_parameters)

		if models.Reports.objects.filter(report_name=new_report_name).exists():
			messages.error(request, f"A report with the name '{new_report_name}' already exists.")
			return redirect('new_report')
		
		new_report = models.Reports.objects.create(report_name=new_report_name)

		i = 0
		for dataset in selected_datasets_ids:
			print(dataset)
			parameter = selected_datasets_parameters[i]
			i+=1
			print(parameter)
			models.Report_Datasets.objects.create(report_id = new_report.id, dataset_id = dataset, report_parameter=parameter)

		return redirect('reports')

def update_parameter_values(request):
	return redirect('datareporting_home')

	