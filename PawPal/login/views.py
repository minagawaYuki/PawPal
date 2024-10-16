from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache

# Create your views here.
@never_cache
def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if(request.user.user_type == 'pet_owner'):
                return redirect('dashboard')
            return redirect('book')
        else:
            error = "Invalid credentials"
            return render(request, 'login/login.html', {'form': form, 'error': error})
    else:
        logout(request)
        form = LoginForm()
    return render(request, 'login/login.html', {'form': form})
