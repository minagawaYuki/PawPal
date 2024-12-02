from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Pet(models.Model):
    pet_name = models.CharField(max_length=100)
    pet_type = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.pet_name} ({self.pet_type})'
    
class Service(models.Model):
    SERVICE_TYPES = (
        ('Pet Boarding', 'Pet Boarding'),
        ('Pet Grooming', 'Pet Grooming'),
        ('Pet Walking', 'Pet Walking'),
    )

    services = models.CharField(max_length=100, choices=SERVICE_TYPES)

    def __str__(self):
        return self.services

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    comment = models.TextField(blank=True, null=True)
    finish_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('canceled', 'Canceled'),
        ('finished', 'Finished')
    ])
    
    def __str__(self):
        return f'Booking {self.id} - {self.pet.pet_name} for {self.service.services} on {self.date}'
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    status = models.CharField(max_length=10, choices=[('unread', 'Unread'), ('read', 'Read')], default='unread')
    notification_type = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message}"


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=255, default=1)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)  # Auto-generated timestamp

    def __str__(self):
        return f"Message from {self.sender} at {self.timestamp}"