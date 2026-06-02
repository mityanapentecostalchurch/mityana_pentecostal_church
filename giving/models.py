from django.db import models


class ContributionCategory(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.name


class Contribution(models.Model):

    PAYMENT_METHODS = [
        ('CASH', 'Cash'),
        ('BANK', 'Bank'),
        ('MOBILE_MONEY', 'Mobile Money'),
    ]

    member = models.ForeignKey(
        'members.Member',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    category = models.ForeignKey(
        ContributionCategory,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        default='CASH'
    )

    reference_number = models.CharField(
        max_length=100,
        blank=True
    )

    contribution_date = models.DateField()

    remarks = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-contribution_date']

    def __str__(self):
        return f"{self.category} - {self.amount}"