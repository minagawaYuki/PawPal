from django.urls import path
from . import views

urlpatterns = [
    path('', views.transactions, name='transactions'),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]