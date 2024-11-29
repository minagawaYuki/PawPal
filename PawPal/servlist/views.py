from django.shortcuts import render, redirect
from .models import Pet, Service, Booking
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Notification
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
import json

@login_required
def dashboard_view(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    bookings = Booking.objects.filter(user_id=request.user.id, status='pending').select_related('pet', 'service')
    past_bookings = Booking.objects.filter(user_id=request.user.id).exclude(status='pending').select_related('pet', 'service')
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    has_new_notifications = notifications.filter(status='unread').exists()

    notifications.filter(status='unread').update(status='read')

    return render(request, 'servlist/user_dashboard.html', {
        'bookings': bookings,
        'past_bookings':past_bookings,
        'notifications': notifications[:5],
        'has_new_notifications': has_new_notifications,
        'first_name': first_name,
        'last_name': last_name,
    })

@login_required
def set_booking_id(request, booking_id):
    request.session['booking_id'] = booking_id
    return redirect('book')


@login_required
def book_schedule(request):
    booking_id = request.session.get('booking_id')
    first_name = request.user.first_name
    last_name = request.user.last_name

    if booking_id:  # Rebooking case
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        # Prepopulate form with data from the existing booking
        context = {
            'date': booking.date,
            'time': booking.time,
            'pet_type': booking.pet.pet_type,
            'pet_name': booking.pet.pet_name,
            'selected_service': booking.service.services,
            'services': Service.objects.all(),
            'first_name': first_name,
            'last_name': last_name,
            'comment': booking.comment,
        }
    else:  # New booking case
        context = {
            'services': Service.objects.all(),
            'first_name': first_name,
            'last_name': last_name,
        }

    if request.method == "POST":
        # Process the form data
        pet_name = request.POST.get('pet_name')
        pet_type = request.POST.get('pet_type')
        service_name = request.POST.get('service')  # Service selected from dropdown
        date = request.POST.get('date')
        time = request.POST.get('time')
        comment = request.POST.get('comment')
        status = 'pending'

        # Check or create the pet
        pet, created = Pet.objects.get_or_create(pet_name=pet_name, pet_type=pet_type)

        # Check if the selected service exists
        try:
            service = Service.objects.get(services=service_name)
        except Service.DoesNotExist:
            return HttpResponse(f"Service '{service_name}' does not exist.")

        # Create a new booking
        Booking.objects.create(
            user=request.user,
            pet=pet,
            service=service,
            date=date,
            time=time,
            comment=comment,
            status=status,
        )

        Notification.objects.create(
            user=request.user,
            message=f"Booking for {pet_name} - {service.services} on {date} at {time} is pending.",
            status='unread',
            notification_type='booking'
        )

        return redirect('dashboard')

    return render(request, 'servlist/booking.html', context)


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




#NEED DATABASE JD
# # Messages
# @login_required
# def messages_view(request):
#     if request.user.is_staff:  # Admin view
#         messages = Message.objects.all().order_by('timestamp')
#     else:  # Pet owner view
#         messages = Message.objects.filter(user=request.user).order_by('timestamp')

#     context = {'messages': messages, 'user': request.user}
#     return render(request, 'servlist/messages.html', context)


# @login_required
# def send_message(request):
#     if request.method == 'POST':
#         content = request.POST.get('message')
#         recipient_username = request.POST.get('recipient')

#         try:
#             recipient = User.objects.get(username=recipient_username)
#         except User.DoesNotExist:
#             return HttpResponse("Recipient not found.")

#         if content:
#             Message.objects.create(
#                 user=request.user,
#                 sender=request.user,
#                 recipient=recipient,
#                 content=content,
#             )
#             return redirect('messages')

#     if request.user.is_staff:
#         users = User.objects.filter(is_staff=False) 
#     else:
#         users = User.objects.filter(is_staff=True)

#     return render(request, 'servlist/send_message.html', {'users': users})

