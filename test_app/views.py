from django.http import HttpResponse
from test_app.models import Test_employees
from django.template.loader import render_to_string

def test_list_view(request):
    # grab the latest 5 rows (ordered by id, descending [-])
   centre_queryset = Test_employees.objects.order_by('-id')[:5]
   context = {"object_list": centre_queryset,}
   HTML_STRING = render_to_string("test_list.html",
   context=context)
   return HttpResponse(HTML_STRING)
