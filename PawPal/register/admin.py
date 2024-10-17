from django.contrib import admin
from .models import CustomUser, Caretaker

admin.site.register(CustomUser)
admin.site.register(Caretaker)
