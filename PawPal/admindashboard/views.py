from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from servlist.models import Booking
from servlist.models import Booking, Notification, Message
from .models import AdminMessage, User
from servlist.models import Booking, Notification
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db.models import Subquery, OuterRef

@login_required
def admin_dashboard(request):
    total_bookings = len(Booking.objects.all())
    active_users = len(User.objects.all())
    total_revenue = 1275 * len(Booking.objects.filter(status='finished'))
    pending_requests = len(Booking.objects.filter(status='pending'))
    recent_bookings = Booking.objects.exclude(status='canceled').order_by('-id')[:10]
    return render(request, 'admindashboard/admin_dashboard.html', {'bookings': bookings,
                                                                   'total_bookings': total_bookings,
                                                                   'active_users': active_users,
                                                                   'total_revenue': total_revenue,
                                                                   'pending_requests': pending_requests,
                                                                   'recent_bookings': recent_bookings})

@login_required
def bookings(request):
    bookings = Booking.objects.filter(status='pending').select_related('user', 'pet', 'service')
    return render(request, 'admindashboard/bookings.html', {'bookings': bookings})

@login_required
def messages(request):
    messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'admindashboard/admin_messages.html', {'messages': messages})

@login_required
def ongoing_bookings(request):
    bookings = Booking.objects.filter(status='accepted').select_related('user', 'pet', 'service').order_by('-id')
    return render(request, 'admindashboard/ongoing_bookings.html', {'bookings': bookings})

@login_required
def finished_bookings(request):
    bookings = Booking.objects.filter(status='finished').select_related('user', 'pet', 'service').order_by('-id')
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
            booking.finish_date = now()
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
        
def admin_messages_view(request):
    latest_messages = Message.objects.filter(
        user=OuterRef('pk')
    ).order_by('-timestamp')
    
    users = (
        User.objects.exclude(is_superuser=True)
        .annotate(
            last_message_content=Subquery(latest_messages.values('content')[:1]),
            last_message_timestamp=Subquery(latest_messages.values('timestamp')[:1])
        )
    )
    return render(request, 'admindashboard/admin_messages.html', {'users': users})

@login_required
def get_user_messages(request, user_id):
    user = get_object_or_404(User, id=user_id)
    messages = Message.objects.filter(user=user).order_by('timestamp')
    last_message = messages.filter(sender='user').last()
    
    data = {
        'username': user.username,
        'messages': [
            {
                'content': message.content,
                'sender': 'admin' if message.sender == 'admin' else 'user',
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            } for message in messages
        ],
        'last_user_message': {
            'content': last_message.content if last_message else None,
            'timestamp': last_message.timestamp.strftime('%Y-%m-%d %H:%M:%S') if last_message else None,
        } if last_message else None
    }
    return JsonResponse(data)

@login_required
def admin_get_messages(request):
    if not request.user.is_staff:  # Ensure the user is an admin
        return JsonResponse({'success': False, 'error': 'Unauthorized access.'}, status=403)

    if request.method == "POST":
        # Admin is sending a reply to a pet owner's message
        data = json.loads(request.body)
        message_id = data.get('message_id')
        reply_content = data.get('reply')

        if message_id and reply_content:
            original_message = get_object_or_404(Message, id=message_id)
            AdminMessage.objects.create(
                receiver=original_message.user,
                sender=request.user.first_name,
                content=reply_content
            )
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error': 'Invalid message ID or content.'})

    # For GET requests, fetch all messages
    pet_owner_messages = Message.objects.all().order_by('timestamp')  # Messages from pet owners
    admin_messages = AdminMessage.objects.all().order_by('timestamp')  # Replies from admin

    # Combine and sort messages by timestamp
    all_messages = sorted(
        list(pet_owner_messages) + list(admin_messages),
        key=lambda x: x.timestamp
    )

    messages = [
        {
            'id': msg.id,
            'sender': msg.sender,
            'receiver': getattr(msg, 'receiver', None).username if isinstance(msg, AdminMessage) else None,
            'content': msg.content,
            'timestamp': msg.timestamp.isoformat()
        }
        for msg in all_messages
    ]

    return JsonResponse({'messages': messages})


@login_required
def get_user_messages(request, user_id):
    user = get_object_or_404(User, id=user_id)
    messages = Message.objects.filter(user=user).order_by('timestamp')
    last_message = messages.filter(sender='user').last()
    
    data = {
        'username': user.username,
        'messages': [
            {
                'content': message.content,
                'sender': 'admin' if message.sender == 'admin' else 'user',
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            } for message in messages
        ],
        'last_user_message': {
            'content': last_message.content if last_message else None,
            'timestamp': last_message.timestamp.strftime('%Y-%m-%d %H:%M:%S') if last_message else None,
        } if last_message else None
    }
    return JsonResponse(data)


@csrf_exempt
@login_required
def reply_to_message(request):
    if request.method == "POST":
        data = json.loads(request.body)
        reply_content = data.get('reply')
        username = data.get('username')

        user = get_object_or_404(User, username=username)
        Message.objects.create(user=user, sender='admin', content=reply_content)
        return JsonResponse({'success': True})
