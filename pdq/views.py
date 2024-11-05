from django.http import FileResponse, HttpResponseRedirect
from . import models
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
	all_sessions = models.AllSessions.objects.all()
	context = {"all_sessions":all_sessions}
	return render(request, "pdq/pdq_allsessions.html", context=context)