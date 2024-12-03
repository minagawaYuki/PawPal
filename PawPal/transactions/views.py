from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from servlist.models import Booking
from django.contrib import messages

# Create your views here.
@login_required
def transactions(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    bookings = Booking.objects.filter(user_id=request.user.id).select_related('pet', 'service').order_by('-id')  # Use select_related to fetch related data efficiently
    return render(request, 'transactions/transactions.html', {'bookings': bookings, 'first_name': first_name, 'last_name': last_name})
@login_required
def cancel_booking(request, booking_id):
    # Ensure this is a POST request
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)

        # Check if booking is already canceled or completed
        if booking.status == 'canceled':
            return JsonResponse({'status': 'error', 'message': 'This booking is already canceled.'})
        else:
            booking.status = 'canceled'
            booking.save()
            return JsonResponse({'status': 'success', 'message': 'Booking canceled successfully.'})

    # If not an AJAX POST request, redirect or show an error
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'}, status=400)
