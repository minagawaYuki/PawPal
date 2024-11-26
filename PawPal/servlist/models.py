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
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('canceled', 'Canceled'),
        ('finished', 'Finished')
    ])
    
    def notify_user_status_change(self):
        # FOR STATUSES
        status_messages = {
            'accepted': f"Your booking for {self.service.services} with {self.pet.pet_name} on {self.date} has been accepted.",
            'canceled': f"Unfortunately, your booking for {self.service.services} with {self.pet.pet_name} on {self.date} was canceled."
        }
        message = status_messages.get(self.status, "Your booking status has been updated.")
    
    def __str__(self):
        return f'Booking {self.id} - {self.pet.pet_name} for {self.service.services} on {self.date}'
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    status = models.CharField(max_length=10, choices=[('unread', 'Unread'), ('read', 'Read')], default='unread')
    notification_type = models.CharField(max_length=50)  # e.g., 'booking', 'status_update'
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message}"