from django.shortcuts import render

# Create your views here.

def admin_dashboard(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, 'admindashboard/admin_dashboard.html')
