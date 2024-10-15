from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from servlist.models import Booking

# Create your views here.
@login_required
def transactions(request):
    first_name = request.user.first_name
    bookings = Booking.objects.filter(user_id=request.user.id).select_related('pet', 'service')  # Use select_related to fetch related data efficiently
    return render(request, 'transactions/transactions.html', {'bookings': bookings, 'first_name': first_name})
