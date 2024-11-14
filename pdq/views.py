from django.http import FileResponse, HttpResponseRedirect
from . import models
from .forms import ResultsDateForm
from django.shortcuts import render, redirect
from django.db.models import Q, QuerySet, Count
from django.utils import timezone
from django.conf import settings
import csv, os
from django.core.paginator import Paginator
PageNotAnInteger = None
EmptyPage = None

def pdq_home(request):
	context = {}
	return render(request, "pdq/pdq_home.html", context=context)

def session_control(request):
	pdq_sessions = models.PDQSessions.objects.filter(visible_session=1).annotate(num_entries=Count('session_entries'))
	context = {"pdq_sessions":pdq_sessions}
	return render(request, "pdq/pdq_pdqsessions.html", context=context)

def add_session(request):
	existing_sessions = models.PDQSessions.objects.filter(visible_session=1).values_list('session_id')
	all_sessions = models.AllSessions.objects.all().exclude(session_id__in=existing_sessions)
	form = ResultsDateForm()
	context = {"all_sessions":all_sessions, "form":form}
	return render(request, "pdq/pdq_addsession.html", context=context)

def add_session_complete(request):
	#form controls
	form = ResultsDateForm(request.POST)
	if form.is_valid():
		cd = form.cleaned_data
	cd_val = cd.get('results_release_datetime')
	session_id = request.POST.get('session')
	if not models.PDQSessions.objects.filter(session_id=session_id).exists():
		models.PDQSessions.objects.create(
			session_id = session_id,
			session_name = models.AllSessions.objects.get(session_id=session_id).session_name,
			session_year = models.AllSessions.objects.get(session_id=session_id).session_year,
			session_sequence = models.AllSessions.objects.get(session_id=session_id).session_sequence,
			results_release_datetime = cd_val
		)
	else:
		models.PDQSessions.objects.filter(session_id=session_id).update(
			results_release_datetime = cd_val,
			visible_session=1
		)
	return redirect('session_control')

def change_session(request, session_id):
	existing_session = models.PDQSessions.objects.get(session_id=session_id)
	form = ResultsDateForm()
	context = {"existing_session":existing_session, "session_id":session_id, "form":form}
	return render(request, "pdq/pdq_changesession.html", context=context)

def remove_session(request, session_id):
	models.PDQSessions.objects.filter(session_id=session_id).update(visible_session=0)
	return redirect('session_control')

def script_requests(request):
	pdqcsv_count = models.PDQStage.objects.filter(csv_download=False).count()
	queryset = models.PDQcsvDownloads.objects.order_by('-uploaded_at')
	print(queryset)
	queryset_paged = Paginator(queryset,20,0,True)
	page_number = request.GET.get('page')
	try:
		page_obj = queryset_paged.get_page(page_number)  # returns the desired page object
	except PageNotAnInteger:
		# if page_number is not an integer then assign the first page
		page_obj = queryset_paged.page(1)
	except EmptyPage:
		# if page is empty then return last page
		page_obj = queryset_paged.page(queryset_paged.num_pages)
	context = {"paged_data": page_obj,"pdqcsv_count":pdqcsv_count}
	return render(request, "pdq/pdq_scriptrequest.html", context=context)

def pdqcsv_create(request):
	pdq_entries = models.PDQEntries.objects.filter(entry_stage__csv_download=False)
	if pdq_entries.count() > 0:
		file_timestamp = timezone.now().strftime("%m_%d_%Y_%H_%M_%S") + ".csv"
		file_location = os.path.join(settings.MEDIA_ROOT, "downloads", file_timestamp).replace('\\', '/')
		print(file_location)
		username = None
		if request.user.is_authenticated:
			username =request.user		
		with open(file_location, 'w', newline='') as file:
			file.truncate()
			writer = csv.writer(file)
			writer.writerow(['Business Stream','Session Month','Session Year','Assessment Code','Component ID','Candidate ID','Candidate Name',
					'Parent Centre','Centre Number','Aggregate Mark','Syllabus Grade','Marker ID','Release Datetime'])
			for s in pdq_entries:
				session_month = s.session_id.session_sequence
				session_year = s.session_id.session_year
				assessment_code = s.syllabus_code
				component_id = s.component_id
				candidate_id = s.candidate_id
				#candidate_name = 
				#parent_centre =
				centre_number = s.centre_number
				#aggregate_mark?
				assessment_grade = s.syllabus_grade
				#marker_id = creditor_number
				release_datetime = s.session_id.results_release_datetime

				writer.writerow(['02',session_month,session_year,assessment_code,component_id,candidate_id,'','',centre_number,"",assessment_grade,"",release_datetime])
				models.PDQStage.objects.filter(entry=s.pk).update(csv_download=True)

		models.PDQcsvDownloads.objects.create(
			document = file_location,
			file_name = file_timestamp,
			download_count = 0,
			archive_count = 0
			)
		
	return redirect('script_requests')

def pdqcsv_download(request, download_id=None):
	# 
	document = models.PDQcsvDownloads.objects.get(pk=download_id).document
	downloads = int(models.PDQcsvDownloads.objects.get(pk=download_id).download_count) + 1
	models.PDQcsvDownloads.objects.filter(pk=download_id).update(download_count = str(downloads))

	return FileResponse(document, as_attachment=True)

