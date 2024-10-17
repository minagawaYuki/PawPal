from django.shortcuts import render

# Create your views here.

def service_listings(request):
    return render(request, 'service_listings/service_listings.html')
