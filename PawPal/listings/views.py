from django.shortcuts import render
from service_listings.models import ServiceListing
# Create your views here.

def listings(request):
    bookings = ServiceListing.objects.all().select_related('user_id')
    return render(request, 'listings/listings.html', {'bookings': bookings})
