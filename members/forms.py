# members/forms.py

from django import forms
from .models import Member


class MemberRegistrationForm(
    forms.ModelForm
):

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