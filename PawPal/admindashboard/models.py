from django.db import models
# Create your models here.
from django.contrib.auth.models import User

class AdminMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_messages_sent')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_messages_received')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)  # Auto-generated timestamp

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username} at {self.timestamp}"

