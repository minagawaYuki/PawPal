from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('bookings/', views.bookings, name='bookings'),
    path('load-bookings/', views.load_bookings, name='load-bookings'),
    path("bookings/accept/", views.accept_booking, name="accept_booking"),
    path("bookings/finish/", views.finish_booking, name="finish_booking"),
    path("bookings/delete/", views.delete_booking, name="delete_booking"),
    path("ongoing_bookings/", views.ongoing_bookings, name="ongoing_bookings"),
    path("finished_bookings/", views.finished_bookings, name="finished_bookings"),
    path('adminMessages/', views.admin_messages_view, name='admin_messages'),
    path('admin-get-messages/', views.admin_get_messages, name='admin-get-messages'),
    path('api/get_user_messages/<int:user_id>/', views.get_user_messages, name='get_user_messages'),
    
]