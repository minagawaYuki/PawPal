from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    is_pet_owner = models.BooleanField(default=False)
    is_caregiver = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='custom_user',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='custom_user',
    )

    def save(self, *args, **kwargs):
        if self.is_pet_owner and self.is_caregiver:
            raise ValueError("User cannot be both Pet Owner and Caregiver.")
        super().save(*args, **kwargs)
