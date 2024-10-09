from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache

# Create your views here.
@never_cache
def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('user_profile')
            else:
                return redirect('register')
        else:
            print(form.errors)
    else:
        logout(request)
        form = LoginForm()
    return render(request, 'login/login.html', {'form': form})
