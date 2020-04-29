from django.forms import ModelForm
from django import forms
from .models import FacilityApplication
from datetime import datetime


class FacilityApplicationForm(ModelForm):
    class Meta:
        model = FacilityApplication
        fields = [
            'alias', 'start', 'end', 'reason',
        ]

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start')
        end = cleaned_data.get('end')

        if start and end:
            if start < datetime.today().date() or \
                end < datetime.today().date():
                raise forms.ValidationError("Application should be at least 24H in advance")

            if end <= start:
                raise forms.ValidationError("Duration must be at least 24H")
