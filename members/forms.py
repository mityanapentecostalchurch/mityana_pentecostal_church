from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from .models import Member


User = get_user_model()


def normalize_phone(phone):
    if not phone:
        return ""

    phone = (
        phone
        .strip()
        .replace(" ", "")
        .replace("-", "")
    )

    if phone.startswith("+256"):
        return phone

    if phone.startswith("256"):
        return "+" + phone

    if phone.startswith("0") and len(phone) == 10:
        return "+256" + phone[1:]

    return phone


class MemberRegistrationForm(forms.ModelForm):

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Create a password",
                "autocomplete": "new-password",
            }
        ),
        validators=[validate_password],
    )

    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm your password",
                "autocomplete": "new-password",
            }
        ),
    )

    class Meta:
        model = Member

        fields = [
            "first_name",
            "last_name",
            "gender",
            "phone_number",
            "email",
        ]

        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter first name",
                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter last name",
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
                    "placeholder": "e.g. 0772123456",
                    "autocomplete": "tel",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Optional",
                    "autocomplete": "email",
                }
            ),
        }

        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "gender": "Gender",
            "phone_number": "Phone Number",
            "email": "Email Address (Optional)",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["gender"].required = True
        self.fields["phone_number"].required = True
        self.fields["email"].required = False

    def clean_phone_number(self):
        phone = self.cleaned_data.get(
            "phone_number"
        )

        phone = normalize_phone(phone)

        if not phone:
            raise forms.ValidationError(
                "Please enter your phone number."
            )

        if not phone.startswith("+256"):
            raise forms.ValidationError(
                "Please enter a valid Ugandan phone number."
            )

        if len(phone) != 13:
            raise forms.ValidationError(
                "Please enter a valid Ugandan phone number."
            )

        if not phone[1:].isdigit():
            raise forms.ValidationError(
                "Please enter a valid phone number."
            )

        if Member.objects.filter(
            phone_number=phone
        ).exists():

            raise forms.ValidationError(
                "An account already exists with this "
                "phone number. Please login instead."
            )

        return phone

    def clean_email(self):
        email = self.cleaned_data.get(
            "email"
        )

        if not email:
            return ""

        email = email.strip().lower()

        if User.objects.filter(
            email__iexact=email
        ).exists():

            raise forms.ValidationError(
                "An account already exists with this "
                "email address."
            )

        return email

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get(
            "password"
        )

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

    def save(self, commit=True):

        member = super().save(
            commit=False
        )

        member.phone_number = normalize_phone(
            self.cleaned_data["phone_number"]
        )

        member.email = (
            self.cleaned_data.get("email")
            or ""
        )

        if commit:
            member.save()

        return member


class MemberProfileForm(forms.ModelForm):

    class Meta:
        model = Member

        exclude = [
            "user",
            "role",
            "status",
            "is_active",
            "created_at",
        ]

        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
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
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "whatsapp_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "next_of_kin": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "next_of_kin_contact": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "village": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "parish": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "sub_county": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "district": forms.TextInput(
                attrs={
                    "class": "form-control",
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
                    "class": "form-select",
                }
            ),

            "number_of_children": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                }
            ),

            "occupation": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "employer": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "place_of_work": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "education_level": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "school_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "is_student": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

            "is_renting": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

            "landlord_name": forms.TextInput(
                attrs={
                    "class": "form-control",
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
                    "class": "form-control",
                }
            ),

            "is_baptized": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
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
                    "class": "form-control",
                }
            ),

            "former_church": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "former_pastor": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "previous_ministry": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "desired_ministry": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "years_at_mpc": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                }
            ),

            "address": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "date_joined": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
        }