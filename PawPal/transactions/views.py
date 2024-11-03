from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from servlist.models import Booking
from django.contrib import messages

# Create your views here.
@login_required
def transactions(request):
    first_name = request.user.first_name
    bookings = Booking.objects.filter(user_id=request.user.id, status='pending').select_related('pet', 'service')  # Use select_related to fetch related data efficiently
    return render(request, 'transactions/transactions.html', {'bookings': bookings, 'first_name': first_name})
@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    # Check if booking is already canceled or completed
    if booking.book_status == 'canceled':
        messages.info(request, "This booking is already canceled.")
    else:
        booking.delete()
        messages.success(request, "Booking canceled successfully.")

    return redirect('dashboard')
