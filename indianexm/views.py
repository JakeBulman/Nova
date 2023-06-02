from django.shortcuts import render

# Create your views here.

# Create your views here.
#@login_required
def indianexm_home_view(request,*args, **kwargs):
	context = {}
	return render(request, "home_indianexm.html", context=context, )
