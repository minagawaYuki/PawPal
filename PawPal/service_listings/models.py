from django.db import models
from register.models import CustomUser

# Create your models here.

class ServiceListing(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.CharField(max_length=40)
    service_type = models.CharField(max_length=40)
    price_per_hour = models.IntegerField()
    location = models.CharField(max_length=40)
    pet_types = models.CharField(max_length=40)
    comment = models.CharField(max_length=40)

    def __str__(self) -> str:
        return self.user_id.username
