from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
@login_required
def dashboard_view(request):
    first_name = request.user.first_name
    return render(request, 'servlist/dashboard.html', {'first_name': first_name})

@login_required
def book_view(request):
    first_name = request.user.first_name
    return render(request, 'servlist/book.html', {'first_name': first_name})