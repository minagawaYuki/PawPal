from django.urls import path
from . import views
from .views import book_schedule

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'), 
    path('book/', views.book_schedule, name='book'),
]