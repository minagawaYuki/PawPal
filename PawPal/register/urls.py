from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('/caregiver_dashboard', views.register, name='register'),
]