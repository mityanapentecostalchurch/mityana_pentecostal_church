from django.db import models
from django.conf import settings


class PrayerRequest(models.Model):

    STATUS_CHOICES = [

        ('PENDING', 'Pending'),

        ('IN_PROGRESS', 'In Progress'),

        ('PRAYED', 'Prayed For'),

        ('COMPLETED', 'Completed'),

    ]

    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=255
    )

    request = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    pastor_comment = models.TextField(
        blank=True
    )

    prayed_by = models.CharField(
        max_length=255,
        blank=True
    )

    prayed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    is_confidential = models.BooleanField(
        default=False
    )

    follow_up_required = models.BooleanField(
        default=False
    )

    answered_testimony = models.TextField(
        blank=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    assigned_to = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.SET_NULL,

        null=True,

        blank=True,

        related_name='assigned_prayers'
    )

    def __str__(self):

        return self.title
    
class PrayerNote(models.Model):

    prayer = models.ForeignKey(
        PrayerRequest,
        on_delete=models.CASCADE,
        related_name='notes'
    )

    staff = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    note = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Note for {self.prayer.title}"