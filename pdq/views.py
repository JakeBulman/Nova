from django.http import FileResponse, HttpResponseRedirect
from . import models
from .forms import ResultsDateForm
from django.shortcuts import render, redirect
from django.db.models import Q, QuerySet, Count


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