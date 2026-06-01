from django.db import models


class Event(models.Model):

    title = models.CharField(max_length=200)

    description = models.TextField()

    event_date = models.DateField()

    event_time = models.TimeField()

    venue = models.CharField(max_length=200)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['event_date']

    def __str__(self):
        return self.title