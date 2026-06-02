from django.db import models

class Service(models.Model):

    SERVICE_TYPES = [
        ('SUNDAY', 'Sunday Worship'),
        ('BIBLE_STUDY', 'Bible Study'),
        ('PRAYER', 'Prayer Meeting'),
        ('YOUTH', 'Youth Service'),
        ('SPECIAL', 'Special Event'),
    ]

    name = models.CharField(
        max_length=100
    )

    service_type = models.CharField(
        max_length=20,
        choices=SERVICE_TYPES
    )

    service_date = models.DateField()
    

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.name} ({self.service_date})"

class Attendance(models.Model):

    ATTENDANCE_STATUS = [
        ('PRESENT', 'Present'),
        ('ABSENT', 'Absent'),
        ('EXCUSED', 'Excused'),
    ]

    member = models.ForeignKey(
        'members.Member',
        on_delete=models.CASCADE
    )

    # service = models.ForeignKey(
    #     'Service',
    #     on_delete=models.CASCADE
    # )

    service = models.ForeignKey(
        'Service',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=ATTENDANCE_STATUS,
        default='PRESENT'
    )

    remarks = models.TextField(
        blank=True
    )

    recorded_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-recorded_at']

    def __str__(self):
        return f"{self.member} - {self.service}"