from django.urls import path
from . import views
from .views import book_schedule, mark_notifications_as_read

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'), 
    path('book/', views.book_schedule, name='book'),
    path('mark_notifications_as_read/', mark_notifications_as_read, name='mark_notifications_as_read'),
    path('update-booking-status/<int:booking_id>/<str:new_status>/', views.update_booking_status, name='update_booking_status'),
    path('book-again/<int:booking_id>/', views.book_again, name='book_again'),
]