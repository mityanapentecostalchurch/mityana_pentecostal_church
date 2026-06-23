from django import forms
from .models import Member


class MemberRegistrationForm(
    forms.ModelForm
):
    
    email = forms.EmailField(
        required=True
    )

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

            'next_of_kin',
            'next_of_kin_contact',

            'number_of_children',

            'occupation',
            'employer',
            'place_of_work',

            'education_level',

            'is_student',
            'school_name',

            'is_baptized',

            'department',
            'desired_ministry',
        ]

class MemberProfileForm(forms.ModelForm):

    class Meta:

        model = Member

        fields = [

            'phone_number',
            'whatsapp_number',

            'address',
            'village',
            'parish',
            'sub_county',
            'district',

            'marital_status',
            'number_of_children',

            'next_of_kin',
            'next_of_kin_contact',

            'occupation',
            'employer',
            'place_of_work',

            'education_level',
            'is_student',
            'school_name',

            'is_renting',
            'landlord_name',

            'date_saved',
            'church_where_saved',

            'is_baptized',
            'baptism_date',
            'baptism_place',

            'former_church',
            'former_pastor',
            'previous_ministry',

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
    
    