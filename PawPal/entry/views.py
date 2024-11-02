from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from django.contrib import messages


def home(request):
    return render(request, "home.html")

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            return redirect('login')
        else:
            return render(request, 'forms/register.html', {'forms': form})

    else:
        form = RegisterForm()
        return render(request, 'forms/register.html', {'forms' : form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'forms/login.html')
    else:
        return render(request, 'forms/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')