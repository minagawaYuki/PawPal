from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('/caregiver_dashboard', views.caregiver_dashboard, name='caregiver_dashboard'),
]