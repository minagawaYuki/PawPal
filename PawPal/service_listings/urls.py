from django.urls import path
from . import views
urlpatterns = [
    path('', views.service_listings, name='service_listings')
]