from django.shortcuts import render

# Create your views here.

def admin_dashboard(request):
    return render(request, 'admindashboard/admin_dashboard.html')