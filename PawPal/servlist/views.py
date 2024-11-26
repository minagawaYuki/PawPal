from django.shortcuts import render, redirect
from .models import Pet, Service, Booking
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Notification
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@login_required
def dashboard_view(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    bookings = Booking.objects.filter(user_id=request.user.id, status='pending').select_related('pet', 'service')
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    has_new_notifications = notifications.filter(status='unread').exists()

    notifications.filter(status='unread').update(status='read')

    return render(request, 'servlist/user_dashboard.html', {
        'bookings': bookings,
        'notifications': notifications[:5],
        'has_new_notifications': has_new_notifications,
        'first_name': first_name,
        'last_name': last_name,
    })


@login_required
def book_schedule(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    if request.method == "POST":
        # Retrieve form data
        pet_name = request.POST.get('pet_name')
        pet_type = request.POST.get('pet_type')
        service_name = request.POST.get('service')  # This matches the service dropdown
        date = request.POST.get('date')
        time = request.POST.get('time')
        status = 'pending'

        # Handle pet: Check if pet already exists; if not, create it
        pet, created = Pet.objects.get_or_create(pet_name=pet_name, pet_type=pet_type)

        # Handle service: Check if the selected service exists
        try:
            service = Service.objects.get(services=service_name)
        except Service.DoesNotExist:
            return HttpResponse(f"Service '{service_name}' does not exist in our system.")

        # Create a new booking
        booking = Booking.objects.create(user=request.user, pet=pet, service=service, date=date, time=time, status=status)
        booking.save()


        Notification.objects.create(
            user=request.user,
            message=f"Booking for {pet_name} - {service.services} on {date} at {time} is pending.",
            status='unread',
            notification_type='booking'
        )


        # Redirect to dashboard after successful booking
        return redirect('dashboard')

    # If GET request, return the booking form with available services
    services = Service.objects.all()  # Fetch available services from the database
    return render(request, 'servlist/booking.html', {'services': services, 'first_name': first_name, 'last_name': last_name})



@login_required
def update_booking_status(request, booking_id, new_status):
    if not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied.'}, status=403)

    try:
        booking = Booking.objects.get(pk=booking_id)
        booking.book_status = new_status
        booking.save()
        booking.notify_user_status_change(new_status)
        return JsonResponse({'success': True})
    except Booking.DoesNotExist:
        return JsonResponse({'error': 'Booking not found.'}, status=404)


@require_POST
@login_required
def mark_notifications_as_read(request):
    Notification.objects.filter(user=request.user, status='unread').update(status='read')
    return JsonResponse({'success': True})




@csrf_exempt
def accept_booking(request):
    if request.method == "POST":
        data = json.loads(request.body)
        booking_id = data.get("booking_id")
        try:
            booking = Booking.objects.get(id=booking_id)
            booking.status = "accepted"
            booking.save()
            
            # Send notification to the pet owner
            booking.notify_user_status_change()
            
            return JsonResponse({"success": True})
        except Booking.DoesNotExist:
            return JsonResponse({"success": False, "error": "Booking not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})


@csrf_exempt
def delete_booking(request):
    if request.method == "POST":
        data = json.loads(request.body)
        booking_id = data.get("booking_id")
        try:
            booking = Booking.objects.get(id=booking_id)
            booking.status = "canceled"
            booking.save()
            
            # Send notification to the pet owner
            booking.notify_user_status_change()
            
            return JsonResponse({"success": True})
        except Booking.DoesNotExist:
            return JsonResponse({"success": False, "error": "Booking not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})