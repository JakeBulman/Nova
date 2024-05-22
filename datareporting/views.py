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
from django.http import HttpResponse
from django.urls import reverse
import psycopg2
import re
from threading import Thread
from django.http import HttpResponse
import subprocess
from django.db.models import OuterRef, Exists
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

PageNotAnInteger = None
EmptyPage = None

# Create your views here.
@login_required
def home_view(request):
	
	report_count = models.Reports.objects.all().count()
	active_report_count = models.Reports.objects.filter(active=True).count()

	dataset_count = models.Datasets.objects.all().count()

	queued_dataset_count = models.ManualTaskQueue.objects.filter(task_queued = 1).count()

	context = {
		'report_count': report_count,
		'active_report_count': active_report_count,
		'dataset_count': dataset_count,
		'queued_dataset_count': queued_dataset_count,
	}


	return render(request, "datareporting/datareporting_home.html", context)


def reports_view(request):
	reports_queryset = models.Reports.objects.all().order_by('id')

	context = {
	'reports_queryset': reports_queryset,
	}
	return render(request, "datareporting/datareporting_reports.html", context)

def datasets_view(request):
	num_queued = Count("task_queue", filter=Q(task_queue__task_queued='1'))
	num_running = Count("task_queue", filter=Q(task_queue__task_running='1'))
	active_dataset = models.Report_Datasets.objects.filter(dataset_id=OuterRef('pk'), report__active=True).values('id')[:1]
	datasets_queryset = models.Datasets.objects.all().annotate(num_queued=num_queued, num_running=num_running, active_dataset=Exists(active_dataset)).order_by('id')
	
	context = {
		'datasets_queryset': datasets_queryset,
		}
	
	return render(request, "datareporting/datareporting_datasets.html", context)

def queue_dataset(request, dataset_id):
	if not models.ManualTaskQueue.objects.filter(dataset=dataset_id, task_queued=1).exists():
		models.ManualTaskQueue.objects.create(
		dataset = models.Datasets.objects.get(id=dataset_id),
		)
		models.Datasets.objects.filter(id=dataset_id).update(last_triggered = timezone.now())

	num_queued = Count("task_queue", filter=Q(task_queue__task_queued='1'))
	num_running = Count("task_queue", filter=Q(task_queue__task_running='1'))
	datasets_queryset = models.Datasets.objects.all().annotate(num_queued=num_queued, num_running=num_running).order_by('id')

	total_num_queued = datasets_queryset.aggregate(total_queued=Sum('num_queued'))['total_queued'] or 0

	context = {
		'datasets_queryset': datasets_queryset,
		'total_num_queued': total_num_queued
		}
	
	return render(request, 'datareporting/partials/datareporting_dataset_cards.html', context)

def run_data_pull(request):

	script_info = models.Script_Info.objects.get(script = 'TASKSQ')
	script_info.running = True
	script_info.start_time = timezone.now()
	script_info.save()
	
	def run_background_script():
		subprocess.run(['python', 'datareporting/script_TASKSQ.py'])

	Thread(target=run_background_script).start()

	return redirect('dataset_processing')

def new_dataset(request):
	return render(request, "datareporting/datareporting_new_dataset.html")

def add_dataset(request):
	if request.method == 'POST':
		dataset_name = request.POST.get('datasetName')
		parameter_name = request.POST.get('parameterName')
		selected_operator = request.POST.get('selectedOperator')
		sql_statement = request.POST.get('sqlStatement')

		sql_statement_lower = sql_statement.lower()

		if " where " in sql_statement_lower:
			messages.error(request, f"Do not include the 'WHERE' clause in your SQL statement.")
		elif " * " in sql_statement_lower:
			messages.error(request, f"The SQL statement must specify all required columns. Do not use 'select *'.")
		elif " limit " in sql_statement_lower:
			messages.error(request, "Do not use the 'LIMIT' function in your SQL statement.")
		elif " join " in sql_statement_lower:
			messages.error(request, "Do not use 'JOIN' function in your SQL statement. This should only include data for a unique table.")
		elif models.Datasets.objects.filter(dataset_name=dataset_name).exists():
			messages.error(request, f"A dataset with the name '{dataset_name}' already exists.")
		else:
			try:
				with pyodbc.connect("DSN=hive.ucles.internal", autocommit=True) as conn:
					pd.read_sql(f'''{sql_statement} limit 0''', conn)

					try:
						table_name_search = re.search(r'(?i)from\s+([^\s;]+)', sql_statement_lower)
						table_name = table_name_search.group(1)
						pd.read_sql(f'''select {parameter_name} from {table_name} limit 0''', conn)

						models.Datasets.objects.create(dataset_name = dataset_name, parameter_name = parameter_name, sql=sql_statement, row_count = 0, operator = selected_operator)
						response = HttpResponse('', status=204)
						response['HX-Redirect'] = request.build_absolute_uri(reverse('datasets'))
						return response
					
					except:
						messages.error(request, f"The parameter is not a valid column of the table {table_name}")

			except Exception as e:
				messages.error(request, f"The SQL statement is not valid: {e}")
			
		all_messages = list(messages.get_messages(request))
		last_message = all_messages[-1] if all_messages else None

		context = {
			'last_message':last_message
		}
			
		return render(request, 'datareporting/partials/datareporting_error_messages.html', context)

def update_report_active_status(request, report_id):
	toggle_status = models.Reports.objects.get(id=report_id).active
	if toggle_status == True:
		toggle_status = False
	else:
		toggle_status = True
	models.Reports.objects.filter(id=report_id).update(active = toggle_status)

def report_datasets(request, report_id):
	report_info = models.Reports.objects.get(id=report_id)
	report_datasets_queryset = models.Report_Datasets.objects.filter(report=report_id).all().order_by('dataset')

	context = {
	'report_info': report_info,
	'report_datasets_queryset': report_datasets_queryset,
	}
	return render(request, "datareporting/datareporting_report_datasets.html", context)

def new_report(request):
	datasets_queryset = models.Datasets.objects.all().order_by('id')

	context = {
	'datasets_queryset': datasets_queryset,
	}
	return render(request, "datareporting/datareporting_new_report.html", context)

def add_report(request):
	if request.method == 'POST':
		new_report_name = request.POST.get('newReportName')
		selected_datasets_ids = request.POST.getlist('selected_dataset')
		
		if models.Reports.objects.filter(report_name=new_report_name).exists():
			messages.error(request, f"A report with the name '{new_report_name}' already exists.")
			
			all_messages = list(messages.get_messages(request))
			last_message = all_messages[-1] if all_messages else None

			context = {
				'last_message':last_message
			}

			return render(request, 'datareporting/partials/datareporting_error_messages.html', context)
		else:
			new_report = models.Reports.objects.create(report_name=new_report_name)
			
			for dataset in selected_datasets_ids:
				parameter = request.POST.get(f'dataset_parameter_{ dataset }')
				models.Report_Datasets.objects.create(report_id = new_report.id, dataset_id = dataset, report_parameter=parameter)

			response = HttpResponse('', status=204)
			response['HX-Redirect'] = request.build_absolute_uri(reverse('reports'))
			return response

def dataset_details(request, dataset_id):
	dataset_info = models.Datasets.objects.get(id=dataset_id)
	reports = models.Report_Datasets.objects.filter(dataset_id=dataset_id)

	context = {
		'dataset_info': dataset_info,
		'reports': reports
	}
	return render(request, "datareporting/datareporting_dataset_details.html", context)

def amend_dataset(request, dataset_id):
	dataset_info = models.Datasets.objects.get(id=dataset_id)

	context = {
		'dataset_info': dataset_info
	}
	return render(request, "datareporting/datareporting_amend_dataset.html", context)

def update_dataset(request, dataset_id):
	if request.method == 'POST':
		new_dataset_name = request.POST.get('newDatasetName')
		new_parameter_name = request.POST.get('newParameterName')
		new_operator = request.POST.get('newSelectedOperator')
		new_sql_statement = request.POST.get('newSqlStatement')
		dataset = models.Datasets.objects.get(id=dataset_id)
		current_dataset_name = dataset.dataset_name

        # Preliminary checks
		sql_statement_lower = new_sql_statement.lower()
		if " where " in sql_statement_lower:
			messages.error(request, f"Do not include the 'WHERE' clause in your SQL statement.")
		elif " * " in sql_statement_lower:
			messages.error(request, f"The SQL statement must specify all required columns. Do not use 'select *'.")
		elif " limit " in sql_statement_lower:
			messages.error(request, "Do not use the 'LIMIT' function in your SQL statement.")
		elif " join " in sql_statement_lower:
			messages.error(request, "Do not use 'JOIN' function in your SQL statement. This should only include data for a unique table.")
		elif new_dataset_name != dataset.dataset_name and models.Datasets.objects.filter(dataset_name=new_dataset_name).exists():
			messages.error(request, f"A dataset with the name '{new_dataset_name}' already exists.")

        # Check for error messages before proceeding
		if not any(msg.level == messages.ERROR for msg in messages.get_messages(request)):
			try:
				with pyodbc.connect("DSN=hive.ucles.internal", autocommit=True) as conn:
					df = pd.read_sql(f'''{new_sql_statement} limit 0''', conn)

					try:
						table_name_search = re.search(r'(?i)from\s+([^\s;]+)', sql_statement_lower)
						table_name = table_name_search.group(1)
						print(f'table name: {table_name}')
						parameter_check = pd.read_sql(f'''select {new_parameter_name} from {table_name} limit 0''', conn)

						dataset.dataset_name = new_dataset_name
						dataset.parameter_name = new_parameter_name
						dataset.operator = new_operator
						dataset.sql = new_sql_statement
						dataset.save()

						conn = psycopg2.connect(dbname='myproject', user='postgres', password='jman', host='localhost')
						cur = conn.cursor()
						if new_dataset_name != dataset.dataset_name:
							cur.execute(f"ALTER TABLE datareporting_dataset_{current_dataset_name} RENAME TO datareporting_dataset_{new_dataset_name}")
						conn.commit()
						cur.close()
						conn.close()

						messages.success(request, f"Dataset Updated Successfully.")

						# Redirect or return an HTMX response after successful update
						response = HttpResponse('', status=204)
						response['HX-Redirect'] = request.build_absolute_uri(reverse('dataset_details', args=[dataset_id]))
						return response

					except:
						messages.error(request, f"The parameter is not a valid column of the table {table_name}")

			except Exception as e:
				messages.error(request, f"An error occurred while updating the dataset: {e}")

        # If there are error messages, collect the last one and render the error message template
		all_messages = list(messages.get_messages(request))
		last_message = all_messages[-1] if all_messages else None

		context = {
            'last_message': last_message,
        }

		return render(request, 'datareporting/partials/datareporting_error_messages.html', context)
		
def update_parameter_values(request, report_id):
	if request.method == 'POST':
		report_datasets = models.Report_Datasets.objects.filter(report_id=report_id)

		for dataset in report_datasets:
			parameter = request.POST.get(f'dataset_parameter_{ dataset.id }')
			dataset.report_parameter = parameter
			dataset.save()

		messages.success(request, 'Dataset values updated successfully.' )

		all_messages = list(messages.get_messages(request))
		last_message = all_messages[-1] if all_messages else None
		message_type = 'Success'

		context = {
			'last_message':last_message,
			'message_type': message_type
		}

		return render(request, "datareporting/partials/datareporting_error_messages.html", context)
	
def amend_report(request, report_id):
	datasets_queryset = models.Datasets.objects.all().order_by('id')
	report_dataset_queryset = models.Report_Datasets.objects.filter(report_id=report_id)
	selected_datasets_ids = models.Report_Datasets.objects.filter(report_id=report_id).values_list('dataset_id', flat=True)
	report_info = models.Reports.objects.get(id=report_id)

	context = {
	'datasets_queryset': datasets_queryset,
	'selected_datasets_ids': list(selected_datasets_ids),
	'report_info': report_info,
	'report_dataset_queryset': report_dataset_queryset
	}

	return render(request, "datareporting/datareporting_amend_report.html", context)

def update_report(request, report_id):
	if request.method == 'POST':
		report = models.Reports.objects.get(id=report_id)
		current_report_name = report.report_name
		new_report_name = request.POST.get('newReportName')
		selected_datasets_ids = request.POST.getlist('selected_dataset')
		
		if current_report_name != new_report_name:
			if models.Reports.objects.filter(report_name=new_report_name).exists():
				messages.error(request, f"A report with the name '{new_report_name}' already exists.")
				
				all_messages = list(messages.get_messages(request))
				last_message = all_messages[-1] if all_messages else None

				context = {
					'last_message':last_message,
				}

				return render(request, 'datareporting/partials/datareporting_error_messages.html', context)

			else:
				report.report_name = new_report_name
				report.save()

		models.Report_Datasets.objects.filter(report_id = report_id).delete()

		for dataset in selected_datasets_ids:
			parameter = request.POST.get(f'dataset_parameter_{ dataset }')
			models.Report_Datasets.objects.create(report_id = report_id, dataset_id = dataset, report_parameter=parameter)
			
		response = HttpResponse('', status=204)
		response['HX-Redirect'] = request.build_absolute_uri(reverse('report_datasets', args=[report_id]))
		return response
	
def delete_dataset_page(request, dataset_id):
	dataset_info = models.Datasets.objects.get(id=dataset_id)
	
	context = {
	'dataset_info': dataset_info,
	}

	return render(request, 'datareporting/datareporting_delete_dataset.html', context)

def confirm_delete_dataset(request, dataset_id):
	dataset = models.Datasets.objects.get(id = dataset_id)
	dataset_name = dataset.dataset_name
	
	check_report_datasets = models.Report_Datasets.objects.filter(dataset_id=dataset_id).exists()

	if check_report_datasets == False:

		dataset.delete()

		conn = psycopg2.connect(dbname='myproject', user='postgres', password='jman', host='localhost')
		cur = conn.cursor()
		cur.execute(f'DROP TABLE IF EXISTS "datareporting_dataset_{dataset_name}"')
		conn.commit()
		cur.close()
		conn.close()

		messages.success(request, f"Dataset '{dataset_name}' successfully deleted.")

	else:
		messages.warning(request, f"Dataset '{dataset_name}' can not be deleted because it is currently being used.")

	return redirect('datasets')

def delete_report_page(request, report_id):
	report_info = models.Reports.objects.get(id=report_id)
	
	context = {
	'report_info': report_info,
	}

	return render(request, 'datareporting/datareporting_delete_report.html', context)

def confirm_delete_report(request, report_id):
	report = models.Reports.objects.get(id = report_id)
	report_name = report.report_name

	report.delete()

	message = messages.success(request, f"Report '{report_name}' successfully deleted.")
	
	return redirect('reports')

def dataset_processing (request):
	queued_datasets = models.ManualTaskQueue.objects.filter(task_queued = 1).order_by('id')

	try:
		currently_processing = models.ManualTaskQueue.objects.get(task_running = 1)
	except ObjectDoesNotExist:
		currently_processing = None

	try:
		script_start_time = models.Script_Info.objects.get(running=True).start_time
		processing_time = timezone.now() - script_start_time
	except ObjectDoesNotExist:
		processing_time = None	

	if request.htmx:

		context = {
		'queued_datasets': queued_datasets,
		'currently_processing': currently_processing,
		'processing_time': processing_time
		}

		return render(request, 'datareporting/partials/datareporting_processing_time.html', context)

	
	datasets_queryset = models.Datasets.objects.all()

	total_num_queued = datasets_queryset.count()
	script_status = models.Script_Info.objects.get(script = 'TASKSQ').running

	context = {
		'queued_datasets': queued_datasets,
		'total_num_queued': total_num_queued,
		'script_status': script_status,
		'currently_processing': currently_processing,
		'processing_time': processing_time
	}

	return render(request, 'datareporting/datareporting_processing.html', context)
