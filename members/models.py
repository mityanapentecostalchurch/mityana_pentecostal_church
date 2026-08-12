from django.db import models
from django.conf import settings


class Role(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.name


class Department(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    leader = models.ForeignKey(
        'Member',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='led_departments'
    )

    def __str__(self):
        return self.name


class Member(models.Model):

    MEMBERSHIP_STATUS = [
        ('ACTIVE', 'Active'),
        ('VISITOR', 'Visitor'),
        ('INACTIVE', 'Inactive'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100
    )

    gender = models.CharField(
        max_length=1,
        choices=[
            ('M', 'Male'),
            ('F', 'Female')
        ]
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=MEMBERSHIP_STATUS,
        default='ACTIVE'
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    # ---------------------------------------------------------
    # Contact Information
    # ---------------------------------------------------------

    whatsapp_number = models.CharField(
        max_length=20,
        blank=True
    )

    next_of_kin = models.CharField(
        max_length=255,
        blank=True
    )

    next_of_kin_contact = models.CharField(
        max_length=20,
        blank=True
    )

    # ---------------------------------------------------------
    # Residence Information
    # ---------------------------------------------------------

    village = models.CharField(
        max_length=100,
        blank=True
    )

    parish = models.CharField(
        max_length=100,
        blank=True
    )

    sub_county = models.CharField(
        max_length=100,
        blank=True
    )

    district = models.CharField(
        max_length=100,
        blank=True
    )

    birthday = models.DateField(
        null=True,
        blank=True
    )

    # ---------------------------------------------------------
    # Family Information
    # ---------------------------------------------------------

    MARITAL_STATUS_CHOICES = [
        ('SINGLE', 'Single'),
        ('MARRIED', 'Married'),
        ('DIVORCED', 'Divorced'),
        ('WIDOWED', 'Widowed'),
    ]

    marital_status = models.CharField(
        max_length=20,
        choices=MARITAL_STATUS_CHOICES,
        blank=True
    )

    number_of_children = models.PositiveIntegerField(
        default=0
    )

    # ---------------------------------------------------------
    # Employment Information
    # ---------------------------------------------------------

    occupation = models.CharField(
        max_length=100,
        blank=True
    )

    employer = models.CharField(
        max_length=255,
        blank=True
    )

    place_of_work = models.CharField(
        max_length=255,
        blank=True
    )

    # ---------------------------------------------------------
    # Education Information
    # ---------------------------------------------------------

    education_level = models.CharField(
        max_length=100,
        blank=True
    )

    is_student = models.BooleanField(
        default=False
    )

    school_name = models.CharField(
        max_length=255,
        blank=True
    )

    is_renting = models.BooleanField(
        default=False
    )

    landlord_name = models.CharField(
        max_length=255,
        blank=True
    )

    # ---------------------------------------------------------
    # Salvation / Church Information
    # ---------------------------------------------------------

    date_saved = models.DateField(
        null=True,
        blank=True
    )

    church_where_saved = models.CharField(
        max_length=255,
        blank=True
    )

    is_baptized = models.BooleanField(
        default=False
    )

    baptism_date = models.DateField(
        null=True,
        blank=True
    )

    baptism_place = models.CharField(
        max_length=255,
        blank=True
    )

    former_church = models.CharField(
        max_length=255,
        blank=True
    )

    former_pastor = models.CharField(
        max_length=255,
        blank=True
    )

    previous_ministry = models.CharField(
        max_length=255,
        blank=True
    )

    desired_ministry = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='interested_members'
    )

    years_at_mpc = models.PositiveIntegerField(
        default=0
    )

    # ---------------------------------------------------------
    # Address / Membership
    # ---------------------------------------------------------

    address = models.CharField(
        max_length=255,
        blank=True
    )

    date_joined = models.DateField(
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# =============================================================
# PHONE OTP
# =============================================================

class PhoneOTP(models.Model):

    phone_number = models.CharField(
        max_length=20
    )

    otp = models.CharField(
        max_length=6
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    expires_at = models.DateTimeField()

    is_verified = models.BooleanField(
        default=False
    )

    attempts = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return f"{self.phone_number} - {self.otp}"