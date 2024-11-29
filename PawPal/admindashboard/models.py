from django.db import models
# Create your models here.
from django.contrib.auth.models import User

# DATABASSEE
# class AdminMessage(models.Model):
#     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_sent_messages')
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Message from {self.sender.username} at {self.timestamp}"
