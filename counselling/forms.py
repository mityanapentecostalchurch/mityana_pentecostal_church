from django import forms
from .models import CounsellingRequest
from accounts.models import User


class CounsellingRequestForm(forms.ModelForm):

    assigned_to = forms.ModelChoiceField(

        queryset=User.objects.filter(
            role='PASTOR'
        ),

        required=False,

        label='Preferred Pastor'
    )

    class Meta:

        model = CounsellingRequest

        fields = [

            'subject',

            'details',

            'assigned_to'

        ]