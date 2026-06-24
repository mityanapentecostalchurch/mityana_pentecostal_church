from django import forms
from .models import PrayerRequest
from accounts.models import User


class PrayerRequestForm(forms.ModelForm):

    class Meta:

        model = PrayerRequest

        fields = [

            'title',

            'request',

            'assigned_to',

            'is_confidential',

        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['assigned_to'].queryset = (
            User.objects.filter(
                is_staff=True
            )
        )