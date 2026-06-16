# reports/models.py

from django.db import models
from members.models import (
    Member,
    Department,
)

class MinistryReport(models.Model):

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )

    submitted_by = models.ForeignKey(
        Member,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=200
    )

    report_text = models.TextField()

    report_month = models.DateField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title