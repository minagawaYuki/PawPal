from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib.auth import logout
from .forms import RegisterForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_type = form.cleaned_data['user_type']
            CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=user_type)
            return redirect('dashboard')
        else:
            print(form.errors)
    else:
        logout(request)
        form = RegisterForm()
    return render(request, 'register/register.html', {'form': form})
