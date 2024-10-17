from django.contrib import admin
from .models import CustomUser, Caretaker, Owner, Booking

admin.site.register(CustomUser)
admin.site.register(Caretaker)
admin.site.register(Owner)
admin.site.register(Booking)