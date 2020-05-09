from datetime import datetime

from django import forms
from django.forms import ModelForm

from .models import FacilityApplication, ResearchApplication


class ApplicationForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start')
        end = cleaned_data.get('end')

        if start and end:
            if start < datetime.today().date() or \
                end < datetime.today().date():
                raise forms.ValidationError("Application should be at least 24H in advance")

            if end <= start:
                raise forms.ValidationError("Duration should be at least 24H")


class FacilityApplicationForm(ApplicationForm):
    class Meta:
        model = FacilityApplication
        fields = (
            'alias', 'start', 'end', 'reason',
        )


class ResearchApplicationForm(ApplicationForm):
    class Meta:
        model = ResearchApplication
        fields = (
            'title', 'start', 'end', 'reason',
        )
