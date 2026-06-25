from django.db import models
from django.conf import settings


class PastoralVisit(models.Model):

    VISIT_TYPES = [

        ('HOME', 'Home Visit'),

        ('HOSPITAL', 'Hospital Visit'),

        ('BEREAVEMENT', 'Bereavement Visit'),

        ('MARRIAGE', 'Marriage Counselling'),

        ('DISCIPLESHIP', 'Discipleship Visit'),

        ('PRAYER', 'Prayer Visit'),

        ('GENERAL', 'General Visit'),

    ]

    STATUS = [

        ('SCHEDULED', 'Scheduled'),

        ('COMPLETED', 'Completed'),

        ('CANCELLED', 'Cancelled'),

    ]

    member = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name='visits'

    )

    pastor = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.SET_NULL,

        null=True,

        related_name='pastoral_visits'

    )

    visit_type = models.CharField(

        max_length=30,

        choices=VISIT_TYPES

    )

    visit_date = models.DateField()

    visit_time = models.TimeField()

    location = models.CharField(

        max_length=255

    )

    purpose = models.TextField()

    notes = models.TextField(

        blank=True

    )

    status = models.CharField(

        max_length=20,

        choices=STATUS,

        default='SCHEDULED'

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    def __str__(self):

        return f"{self.member} - {self.visit_type}"