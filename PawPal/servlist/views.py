from django.shortcuts import render, redirect
from .models import Pet, Service, Booking
from django.http import HttpResponse

def dashboard_view(request):
    # Fetch all bookings
    bookings = Booking.objects.all().select_related('pet', 'service')  # Use select_related to fetch related data efficiently
    return render(request, 'servlist/dashboard.html', {'bookings': bookings})

def book_schedule(request):
    if request.method == "POST":
        # Retrieve form data
        pet_name = request.POST.get('pet_name')
        pet_type = request.POST.get('pet_type')
        service_name = request.POST.get('service')  # This matches the service dropdown
        date = request.POST.get('date')
        time = request.POST.get('time')

        # Handle pet: Check if pet already exists; if not, create it
        pet, created = Pet.objects.get_or_create(pet_name=pet_name, pet_type=pet_type)

        # Handle service: Check if the selected service exists
        try:
            service = Service.objects.get(services=service_name)
        except Service.DoesNotExist:
            return HttpResponse(f"Service '{service_name}' does not exist in our system.")

        # Create a new booking
        booking = Booking.objects.create(pet=pet, service=service, date=date, time=time)
        booking.save()

        # Redirect to dashboard after successful booking
        return redirect('dashboard')

    # If GET request, return the booking form with available services
    services = Service.objects.all()  # Fetch available services from the database
    return render(request, 'servlist/book.html', {'services': services})