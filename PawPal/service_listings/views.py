from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from .forms import ServiceListingForm
# Create your views here.

@never_cache
def service_listings(request):
    if request.method == 'POST':
        form = ServiceListingForm(request.POST)
        if form.is_valid():

            service_listing = form.save(commit=False)
            service_listing.user_id = request.user
            service_listing.save()

    form = ServiceListingForm()

    return render(request, 'service_listings/service_listings.html', {'form': form, 'user': request.user})
