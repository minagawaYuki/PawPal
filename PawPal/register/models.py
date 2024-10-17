from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django import forms

class CustomerUserManager(BaseUserManager):
    def create_user(self, username, first_name=None, last_name=None, email=None, phone_number=None, address=None, user_type=None, password=None, **extra_fields):
        if not username:
            raise ValueError("Username must be set")
        user = self.model(username=username, first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, address=address, user_type=user_type)
        user.set_password(password)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', False)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password, user_type, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(username, password)
    
    def get_by_natural_key(self, username: str | None):
        return self.get(username=username)

class CustomUser(AbstractBaseUser):
    USER_TYPES = (
        ('owner', 'Pet Owner'),
        ('caretaker', 'Pet Caretaker'),
    )
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    username = models.CharField(max_length=40, unique=True)
    password = models.CharField(max_length=40)
    phone_number = models.CharField(max_length=40, unique=True, null=True)
    email = models.EmailField()
    address = models.CharField(max_length=40, null=True)
    user_type = models.CharField(max_length=40, choices=USER_TYPES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = CustomerUserManager()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["user_type"]

    def has_perm(self, perm, obj=None):
        return self.is_staff
    
    def has_module_perms(self, app_label):
        return self.is_staff
    
class Caretaker(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    successful_bookings = models.IntegerField(null=True)
    experience = models.IntegerField(null=True)

    def __str__(self) -> str:
        return self.user.username
    
class Owner(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username
    
class Booking(models.Model):
    pet_owner = models.ForeignKey('Owner', on_delete=models.CASCADE)
    caretaker = models.ForeignKey('Caretaker', on_delete=models.CASCADE)
    service_type = models.CharField(max_length=50)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=50)
    total_price = models.IntegerField()

    def __str__(self) -> str:
        return self.pet_owner.username
    

