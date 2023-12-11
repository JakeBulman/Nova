from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


def login_user(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if username == 'RPABOT':
                return redirect('rpa_apportionment')
            elif username == 'RPABOT2' or username == 'RPABOT3':
                return redirect('rpa_marks_keying')
            else:
                return redirect('home')
        else:
            # Return an 'invalid login' error message
            messages.success(request,("There was an error logging in, please try again."))
            return redirect('login')
    else:
        return render(request, 'nova_core/user_login.html', {})

def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'authenticate/register_user.html', {
        'form':form,
    })

def logout_user(request):
    logout(request)
    messages.success(request,("You have logged out."))
    return redirect('home')
