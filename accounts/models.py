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

    # --------------------------
    # NEW PROFILE INFORMATION
    # --------------------------

    profile_photo = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )
    # profile_photo = models.URLField(
    #     blank=True,
    #     null=True
    # )

    position = models.CharField(
        max_length=120,
        blank=True
    )

    biography = models.TextField(
        blank=True
    )

    office = models.CharField(
        max_length=150,
        blank=True
    )

    department = models.CharField(
        max_length=120,
        blank=True
    )

    facebook = models.URLField(
        blank=True,
        null=True
    )

    youtube = models.URLField(
        blank=True,
        null=True
    )

    whatsapp = models.CharField(
        max_length=20,
        blank=True
    )

    date_joined_ministry = models.DateField(
        blank=True,
        null=True
    )
    is_head_leader = models.BooleanField(
        default=False,
        help_text="Check this for the Senior Pastor or overall head of the church."
    )

    def full_name(self):

        return f"{self.first_name} {self.last_name}"

    def __str__(self):

        return f"{self.first_name} {self.last_name} ({self.role})"