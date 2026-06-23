from django import forms
from .models import PrayerRequest


class PrayerRequestForm(forms.ModelForm):

    class Meta:

        model = PrayerRequest

        fields = [

            'title',

            'request',

        ]