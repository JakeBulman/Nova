'''
from django.shortcuts import render
from .forms import EmployeeForm

def index(request):
    form = EmployeeForm()
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'employee_form.html', context)
'''
def home_view(request):
    from http.client import HTTPResponse
    from models import Employee

    employee_obj = Employee.objects.get(id=1)

    return HTTPResponse("<h1>Hello</h1>")
