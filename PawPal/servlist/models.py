from django.db import models

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
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    
    def __str__(self):
        return f'Booking for Pet {self.pet.pet_name} - {self.service.services} on {self.date} at {self.time}'