from django.shortcuts import render

# Create your views here.
def dashboard_view(request):
    return render(request, 'servlist/dashboard.html')

def book_view(request):
    return render(request, 'servlist/book.html')