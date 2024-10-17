from django import forms
from .models import ServiceListing

class ServiceListingForm(forms.ModelForm):
    class Meta:
        model = ServiceListing
        fields = ['description', 'service_type', 'price_per_hour', 'location', 'pet_types'] 