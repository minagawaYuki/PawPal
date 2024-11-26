from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from servlist.models import Booking
from servlist.models import Booking, Notification

@login_required
def admin_dashboard(request):
    bookings = Booking.objects.filter(status='pending').select_related('user', 'pet', 'service')
    return render(request, 'admindashboard/admin_dashboard.html', {'bookings': bookings})

@login_required
def bookings(request):
    bookings = Booking.objects.filter(status='pending').select_related('user', 'pet', 'service')
    return render(request, 'admindashboard/admin_dashboard.html', {'bookings': bookings})

@login_required
def ongoing_bookings(request):
    bookings = Booking.objects.filter(status='accepted').select_related('user', 'pet', 'service')
    return render(request, 'admindashboard/ongoing_bookings.html', {'bookings': bookings})

@login_required
def finished_bookings(request):
    bookings = Booking.objects.filter(status='finished').select_related('user', 'pet', 'service')
    return render(request, 'admindashboard/finished_bookings.html', {'bookings': bookings})

@login_required
def load_bookings(request):
    try:
        # Remove the user filter to get all bookings
        bookings = Booking.objects.all().select_related('user', 'pet', 'service')
        booking_data = []
        
        for booking in bookings:
            booking_data.append({
                'id': booking.id,
                'user': {
                    'first_name': booking.user.first_name,
                    'last_name': booking.user.last_name,
                },
                'service': booking.service.name if booking.service else '',
                'pet_type': booking.pet.pet_type if booking.pet else '',
                'date': booking.date.strftime('%m/%d/%Y') if booking.date else '',
                'time': booking.time.strftime('%I:%M %p') if booking.time else '',
                'status': booking.status if hasattr(booking, 'status') else 'pending'
            })
        
        return JsonResponse({
            'status': 'success',
            'bookings': booking_data
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@csrf_exempt
def accept_booking(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            booking_id = data.get("booking_id")

            booking = Booking.objects.get(id=booking_id)
            booking.status = "accepted"
            booking.save()

            # Ensure that the service and pet exist before accessing their attributes
            service_name = booking.service.services if booking.service else "Unknown Service"
            pet_name = booking.pet.pet_name if booking.pet else "Unknown Pet"

            # Create a notification for the pet owner
            Notification.objects.create(
                user=booking.user,
                message=f"Your booking for {pet_name} - {service_name} on {booking.date} at {booking.time} has been accepted.",
                status='unread',
                notification_type='booking_update'
            )

            return JsonResponse({"success": True})
        except Booking.DoesNotExist:
            return JsonResponse({"success": False, "error": "Booking not found"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

@csrf_exempt
def finish_booking(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            booking_id = data.get("booking_id")

            booking = Booking.objects.get(id=booking_id)
            booking.status = "finished"
            booking.save()

            service_name = booking.service.services if booking.service else "Unknown Service"
            pet_name = booking.pet.pet_name if booking.pet else "Unknown Pet"

            Notification.objects.create(
                user=booking.user,
                message=f"Your booking for {pet_name} - {service_name} on {booking.date} at {booking.time} has been marked as finished.",
                status='unread',
                notification_type='booking_update'
            )

            return JsonResponse({"success": True})
        except Booking.DoesNotExist:
            return JsonResponse({"success": False, "error": "Booking not found"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

@csrf_exempt
def delete_booking(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            booking_id = data.get("booking_id")

            booking = Booking.objects.get(id=booking_id)
            booking.status = "canceled"
            booking.save()

            service_name = booking.service.services if booking.service else "Unknown Service"
            pet_name = booking.pet.pet_name if booking.pet else "Unknown Pet"

            Notification.objects.create(
                user=booking.user,
                message=f"Your booking for {pet_name} - {service_name} on {booking.date} at {booking.time} has been canceled.",
                status='unread',
                notification_type='booking_update'
            )

            return JsonResponse({"success": True})
        except Booking.DoesNotExist:
            return JsonResponse({"success": False, "error": "Booking not found"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)