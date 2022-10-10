from django.http import HttpResponse
from centres.models import Centres
from django.template.loader import render_to_string
def centre_list_view(request):

    # grab the latest 5 rows (ordered by id, descending [-]
   centre_queryset = Centres.objects.order_by('-id')[:5]
   context = {"object_list": centre_queryset,}

   HTML_STRING = render_to_string("centres_list.html",
   context=context)
   return HttpResponse(HTML_STRING)


from django.shortcuts import render
from .forms import CentresForm

def centre_form_view(request):
	context ={}

	form = CentresForm(request.POST or None)
	
	if form.is_valid():
		form.save()
		form = CentresForm()

	context['form']= form
	return render(request, "centres_form.html", context)
