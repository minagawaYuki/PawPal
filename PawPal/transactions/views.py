from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from servlist.models import Booking
from django.contrib import messages
from django.http import JsonResponse

@login_required
def transactions(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    bookings = Booking.objects.filter(user_id=request.user.id, status='pending').select_related('pet', 'service')
    return render(request, 'transactions/transactions.html', {'bookings': bookings, 'first_name': first_name, 'last_name': last_name})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if booking.book_status == 'canceled':
        message = "This booking is already canceled."
        if is_ajax:
            return JsonResponse({'status': 'error', 'message': message})
        messages.info(request, message)
    else:
        try:
            booking.book_status = 'canceled'
            booking.save()
            message = "Booking canceled successfully."
            if is_ajax:
                return JsonResponse({'status': 'success', 'message': message})
            messages.success(request, message)
        except Exception as e:
            message = "An error occurred while canceling the booking."
            if is_ajax:
                return JsonResponse({'status': 'error', 'message': str(e)})
            messages.error(request, message)

    if is_ajax:
        return JsonResponse({'status': 'error', 'message': 'Unknown error occurred'})
    return redirect('transactions')