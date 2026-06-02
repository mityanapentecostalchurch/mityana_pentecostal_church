from django.db import models


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

    service_date = models.DateField()

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
        ordering = ['-service_date']

    def __str__(self):
        return f"{self.member} - {self.service_date}"