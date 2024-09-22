from django.shortcuts import render

# Create your views here.
def service_listings(request):
    print("service_listings view called")
    return render(request, 'servlist/servicelisting.html')