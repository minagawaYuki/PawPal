from django.shortcuts import render, redirect
from .models import Pet, Service, Booking
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def dashboard_view(request):
    # Fetch all bookings
    first_name = request.user.first_name
    bookings = Booking.objects.filter(user_id=request.user.id).select_related('pet', 'service')  # Use select_related to fetch related data efficiently
    return render(request, 'servlist/index.html', {'bookings': bookings, 'first_name': first_name})

@login_required
def book_schedule(request):
    first_name = request.user.first_name
    if request.method == "POST":
        # Retrieve form data
        pet_name = request.POST.get('pet_name')
        pet_type = request.POST.get('pet_type')
        service_name = request.POST.get('service')
        date = request.POST.get('date')
        time = request.POST.get('time')
        comment = request.POST.get('comment')  # Retrieve the comment

        # Handle pet: Check if pet already exists; if not, create it
        pet, created = Pet.objects.get_or_create(pet_name=pet_name, pet_type=pet_type)

        # Handle service: Check if the selected service exists
        try:
            service = Service.objects.get(services=service_name)
        except Service.DoesNotExist:
            return HttpResponse(f"Service '{service_name}' does not exist in our system.")

        # Create a new booking with the comment
        booking = Booking.objects.create(user=request.user, pet=pet, service=service, date=date, time=time, comment=comment)
        booking.save()

        # Redirect to dashboard after successful booking
        return redirect('dashboard')

    # If GET request, return the booking form with available services
    services = Service.objects.all()
    return render(request, 'servlist/booking.html', {'services': services, 'first_name': first_name})



#GAMITA NI MAARRRK PRA MO GAWAS ANG COMMENT SA ADMINDASHBOARD
#<p><b>Comment:</b> {{ booking.comment }}</p>




@login_required
def mark_as_finished(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
        booking.status = 'Finished'
        booking.save()
        return redirect('dashboard')
    except Booking.DoesNotExist:
        return HttpResponse("Booking does not exist.")