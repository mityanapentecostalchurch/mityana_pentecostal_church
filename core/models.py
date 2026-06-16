from django.db import models

class ChurchLeader(models.Model):

    POSITION_CHOICES = [
        ('LEAD_PASTOR', 'Lead Pastor'),
        ('ASSOCIATE_PASTOR', 'Associate Pastor'),
        ('ELDER', 'Elder'),
        ('DEACON', 'Deacon'),
        ('SECRETARY', 'Secretary'),
        ('TREASURER', 'Treasurer'),
        ('YOUTH_PASTOR', 'Youth Pastor'),
        ('WOMEN_LEADER', 'Women Leader'),
        ('MEN_LEADER', 'Men Leader'),
        ('CHOIR_LEADER', 'Choir Leader'),
    ]

    full_name = models.CharField(
        max_length=200
    )

    position = models.CharField(
        max_length=50,
        choices=POSITION_CHOICES
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    photo = models.ImageField(
        upload_to='leaders/',
        blank=True,
        null=True
    )

    biography = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.full_name