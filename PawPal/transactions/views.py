from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def transactions(request):
    return render(request, 'transactions/transactions.html')
