from django import forms
from .models import Member


class MemberRegistrationForm(
    forms.ModelForm
):

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )

    class Meta:

        model = Member

        fields = [

            'first_name',
            'last_name',

            'gender',

            'birthday',

            'phone_number',

            'whatsapp_number',

            'email',

            'address',

            'village',

            'parish',

            'sub_county',

            'district',

            'marital_status',

            'occupation',

            'department',

            'desired_ministry',

        ]

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get(
            'password'
        )

        confirm_password = cleaned_data.get(
            'confirm_password'
        )

        if password != confirm_password:

            raise forms.ValidationError(
                "Passwords do not match."
            )

        return cleaned_data