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


# NEEDED DATABASE
# class Message(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
#     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_sent_messages')
#     recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', null=True) # non-nullable field pani siya, tan.awa lng unsa possible error
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set the timestamp kuyaw kaysa

#     def __str__(self):
#         return f"Message from {self.sender.username} to {self.recipient.username} at {self.timestamp}"

