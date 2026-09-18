from django import forms
from accounts.models import User
from members.models import Department


class StaffCreateForm(forms.ModelForm):

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter password"
            }
        )
    )

    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm password"
            }
        )
    )

    class Meta:
        model = User

        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_number",
            "role",
            "position",
            "department",
            "office",
            "biography",
            "profile_photo",
            "is_active",
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

            "username": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "role": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "position": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "department": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "office": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "biography": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4
                }
            ),

            "profile_photo": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),
        }

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError(
                    "The passwords do not match."
                )

        return cleaned_data

    def save(self, commit=True):

        user = super().save(commit=False)

        password = self.cleaned_data.get("password")

        user.set_password(password)

        if commit:
            user.save()

        return user


class StaffUpdateForm(forms.ModelForm):

    class Meta:
        model = User

        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_number",
            "role",
            "position",
            "department",
            "office",
            "biography",
            "profile_photo",
            "is_active",
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

            "username": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "role": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "position": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "department": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "office": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "biography": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4
                }
            ),

            "profile_photo": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),
        }

class DepartmentForm(forms.ModelForm):

    class Meta:

        model = Department

        fields = [
            "name",
            "description",
            "leader",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter department name"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Describe the department"
                }
            ),

            "leader": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

        }

        labels = {

            "name": "Department Name",

            "description": "Description",

            "leader": "Department Leader",

        }
