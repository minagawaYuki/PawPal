from django.db import models

# Create your models here.

class chat(models.Model):
    message = models.CharField(max_length=100)
    # date = models.DateField()
    # time = models.IntegerField()
    

class register(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=59)
    email = models.EmailField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)