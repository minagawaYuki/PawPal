from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('book/', views.book_schedule, name='book'),
    path('set-booking-id/<int:booking_id>/', views.set_booking_id, name='set_booking_id'),  # New URL to set booking_id in session
    path('mark_notifications_as_read/', views.mark_notifications_as_read, name='mark_notifications_as_read'),
    path('update-booking-status/<int:booking_id>/<str:new_status>/', views.update_booking_status, name='update_booking_status'),
]

# path('messages/', views.messages_view, name='messages'),