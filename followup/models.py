from django.db import models
from django.conf import settings


class MemberFollowUp(models.Model):

    STATUS_CHOICES = [

        ('PENDING', 'Pending'),

        ('ONGOING', 'Ongoing'),

        ('COMPLETED', 'Completed'),

    ]

    FOLLOWUP_TYPES = [

        ('NEW_MEMBER', 'New Member'),

        ('VISITOR', 'Visitor'),

        ('HOME_VISIT', 'Home Visit'),

        ('HOSPITAL', 'Hospital Visit'),

        ('BEREAVEMENT', 'Bereavement'),

        ('ABSENT_MEMBER', 'Absent Member'),

        ('GENERAL', 'General'),

    ]

    member = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name='followups'

    )

    assigned_to = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.SET_NULL,

        null=True,

        blank=True,

        related_name='assigned_followups'

    )

    followup_type = models.CharField(

        max_length=30,

        choices=FOLLOWUP_TYPES,

        default='GENERAL'

    )

    reason = models.TextField()

    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default='PENDING'

    )

    pastor_notes = models.TextField(

        blank=True

    )

    visit_required = models.BooleanField(
        default=False
    )

    visit_type = models.CharField(
        max_length=30,
        blank=True
    )

    visit_date = models.DateField(
        null=True,
        blank=True
    )

    visit_time = models.TimeField(
        null=True,
        blank=True
    )

    visit_location = models.CharField(
        max_length=255,
        blank=True
    )

    visit_completed = models.BooleanField(
        default=False
    )

    visit_date = models.DateField(

        null=True,

        blank=True

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    updated_at = models.DateTimeField(

        auto_now=True

    )

    def __str__(self):

        return f"{self.member.username} - {self.followup_type}"
    
class MemberNotification(models.Model):

    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    title = models.CharField(
        max_length=255
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title
    
