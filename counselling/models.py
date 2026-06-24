from django.db import models
from django.conf import settings


class CounsellingRequest(models.Model):

    STATUS_CHOICES = [

        ('PENDING', 'Pending'),

        ('SCHEDULED', 'Scheduled'),

        ('COMPLETED', 'Completed'),

    ]

    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='counselling_requests'
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_counselling'
    )

    subject = models.CharField(
        max_length=255
    )

    details = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    pastor_notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    scheduled_date = models.DateField(
        null=True,
        blank=True
    )

    scheduled_time = models.TimeField(
        null=True,
        blank=True
    )

    location = models.CharField(
        max_length=255,
        blank=True
    )

    def __str__(self):

        return self.subject