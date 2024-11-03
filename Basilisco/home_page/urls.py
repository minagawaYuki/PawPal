from django.urls import path 
from . import views

urlpatterns = [
    path("main_page", views.main_page, name='main_page'),
    path("service", views.services, name='service'),
]