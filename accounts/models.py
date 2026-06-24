from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    USER_TYPES = [

        ('STAFF', 'Staff'),

        ('VISITOR', 'Visitor'),

    ]

    ROLE_CHOICES = [

        ('MEMBER', 'Member'),

        ('PASTOR', 'Pastor'),

        ('SECRETARY', 'Secretary'),

        ('TREASURER', 'Treasurer'),

        ('MINISTRY_LEADER', 'Ministry Leader'),

        ('INTERCESSOR', 'Intercessor'),

        ('SUPER_ADMIN', 'Super Admin'),

    ]

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPES,
        default='VISITOR'
    )

    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        default='MEMBER'
    )

    # def __str__(self):

        # return self.username
    
    def __str__(self):

        return (
            f"{self.first_name} "
            f"{self.last_name}"
            f" ({self.role})"
        )