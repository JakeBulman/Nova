from django.shortcuts import render
from django.http import FileResponse
from . import models
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator
from django.conf import settings
import csv, os, pathlib
from django.utils.datastructures import MultiValueDict

# Create your views here.

# Create your views here.
@login_required
def indianexm_home_view(request,*args, **kwargs):
	context = {}
	return render(request, "home_indianexm.html", context=context, )

def indianexm_upload_view(request,*args, **kwargs):
	context = {}
	return render(request, "indianexm_upload.html", context=context, )

def indianexm_single_file_upload_view(request):
    data = MultiValueDict(request.FILES).getlist('filename')
    file_counter = 1
    for file in data:
        file_timestamp = timezone.now().strftime("%m_%d_%Y_%H_%M_%S") + str(file_counter) + ".csv"
        file_location = os.path.join(settings.MEDIA_ROOT, "indianexaminer_uploads", file_timestamp).replace('\\', '/')
        destination = open(file_location, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()

        file_counter += 1

        models.IndexmUploads.objects.create(
            document = file_location,
            file_name = file,
            )
    
    return redirect('indianexm_upload')
