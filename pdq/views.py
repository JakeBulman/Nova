from django.http import FileResponse, HttpResponseRedirect
from . import models
from .forms import ResultsDateForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q, QuerySet
from django.conf import settings
import csv, os
from django.db.models import Sum, Count
from django.contrib.auth.models import User
from django.db.models.functions import Cast, Substr
import dateutil.parser
from django.db.models import OuterRef, Subquery, Max
from datetime import datetime, timedelta, time

def pdq_home(request):
	context = {}
	return render(request, "pdq/pdq_home.html", context=context)

def session_control(request):
	pdq_sessions = models.PDQSessions.objects.all()
	context = {"pdq_sessions":pdq_sessions}
	return render(request, "pdq/pdq_pdqsessions.html", context=context)

def add_session(request):
	all_sessions = models.AllSessions.objects.all()
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
	print(cd_val)
	print(session_id)
	models.PDQSessions.objects.create(
		session_id = session_id,
		session_name = models.AllSessions.objects.get(session_id=session_id).session_name,
		session_year = models.AllSessions.objects.get(session_id=session_id).session_year,
		session_sequence = models.AllSessions.objects.get(session_id=session_id).session_sequence,
		results_release_datetime = cd_val
	)
	return redirect('session_control')