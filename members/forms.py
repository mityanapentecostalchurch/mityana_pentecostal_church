# members/forms.py

from django import forms
from django.contrib.auth import get_user_model

from .models import Member


User = get_user_model()


# ============================================================
# MEMBER REGISTRATION FORM
# ============================================================

class MemberRegistrationForm(forms.ModelForm):

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Create a password",
            }
        ),
        min_length=6,
        required=True,
    )

    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm your password",
            }
        ),
        required=True,
    )

    class Meta:

        model = Member

        fields = [
            "first_name",
            "last_name",
            "gender",
            "phone_number",
            "email",
            "address",
        ]

        widgets = {

            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your first name",
                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your last name",
                }
            ),

            "gender": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. 0700123456",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Optional: yourname@gmail.com",
                }
            ),

            "address": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Village / Address",
                }
            ),
        }

        labels = {

            "first_name": "First Name",

            "last_name": "Last Name",

            "gender": "Gender",

            "phone_number": "Mobile Phone Number",

            "email": "Email Address (Optional)",

            "address": "Address",
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Email is OPTIONAL
        self.fields["email"].required = False

        # Phone number is REQUIRED
        self.fields["phone_number"].required = True

    def clean_phone_number(self):

        phone = self.cleaned_data.get("phone_number")

        if not phone:

            raise forms.ValidationError(
                "Mobile phone number is required."
            )

        # Remove spaces and hyphens
        phone = (
            phone
            .strip()
            .replace(" ", "")
            .replace("-", "")
        )

        # Convert +256XXXXXXXXX to 0XXXXXXXXX
        if phone.startswith("+256"):

            phone = "0" + phone[4:]

        # Convert 256XXXXXXXXX to 0XXXXXXXXX
        elif phone.startswith("256"):

            phone = "0" + phone[3:]

        # Basic Ugandan mobile validation
        if not phone.startswith("07"):

            raise forms.ValidationError(
                "Please enter a valid Ugandan mobile number, "
                "for example 0700123456."
            )

        if len(phone) != 10:

            raise forms.ValidationError(
                "A Ugandan mobile number should contain 10 digits."
            )

        if not phone.isdigit():

            raise forms.ValidationError(
                "Phone number should contain numbers only."
            )

        # Check for an existing member
        if Member.objects.filter(
            phone_number=phone
        ).exists():

            raise forms.ValidationError(
                "This phone number is already registered. "
                "Please use the login option instead."
            )

        return phone

    def clean_email(self):

        email = self.cleaned_data.get("email")

        # Email is optional
        if not email:

            return ""

        email = email.strip().lower()

        # Check existing account
        if User.objects.filter(
            email__iexact=email
        ).exists():

            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get("password")

        confirm_password = cleaned_data.get(
            "confirm_password"
        )

        if password and confirm_password:

            if password != confirm_password:

                self.add_error(
                    "confirm_password",
                    "The passwords do not match."
                )

        return cleaned_data


# ============================================================
# MEMBER PROFILE FORM
# ============================================================

class MemberProfileForm(forms.ModelForm):

    class Meta:

        model = Member

        fields = [

            "first_name",
            "last_name",
            "gender",

            "phone_number",
            "email",
            "whatsapp_number",

            "next_of_kin",
            "next_of_kin_contact",

            "village",
            "parish",
            "sub_county",
            "district",

            "birthday",

            "marital_status",
            "number_of_children",

            "occupation",
            "employer",
            "place_of_work",

            "education_level",
            "is_student",
            "school_name",

            "is_renting",
            "landlord_name",

            "date_saved",
            "church_where_saved",

            "is_baptized",
            "baptism_date",
            "baptism_place",

            "former_church",
            "former_pastor",
            "previous_ministry",

            "desired_ministry",
            "years_at_mpc",

            "address",
        ]

        widgets = {

            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "gender": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "whatsapp_number": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "next_of_kin": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "next_of_kin_contact": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "village": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "parish": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "sub_county": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "district": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "birthday": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "marital_status": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "number_of_children": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                }
            ),

            "occupation": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "employer": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "place_of_work": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "education_level": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "is_student": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),

            "school_name": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "is_renting": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),

            "landlord_name": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "date_saved": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "church_where_saved": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "is_baptized": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),

            "baptism_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "baptism_place": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "former_church": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "former_pastor": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "previous_ministry": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "desired_ministry": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "years_at_mpc": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                }
            ),

            "address": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),
        }