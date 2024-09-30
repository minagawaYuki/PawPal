from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def register_user(request):
    return render(request, 'registrationform.html')

def login_user(request):
    return render(request, 'login.html')

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('login.html')
    return render(request, 'login.html')

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import RegisterForm
from .models import UserProfile

def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            UserProfile.objects.create(user=user, role=form.cleaned_data['role'])

            login(request, user)
            return redirect('login.html')
    else:
        form = RegisterForm()
    return render(request, 'registerform.html', {'form': form})
