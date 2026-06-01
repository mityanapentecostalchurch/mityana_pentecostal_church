# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = [
        ('SUPER_ADMIN', 'Super Admin'),
        ('PASTOR', 'Pastor'),
        ('TREASURER', 'Treasurer'),
        ('SECRETARY', 'Secretary'),
        ('MEDIA', 'Media Team'),
        ('MEMBER', 'Member'),
    ]

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='MEMBER'
    )

    def __str__(self):
        return self.username