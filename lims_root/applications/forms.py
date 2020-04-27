from django.forms import ModelForm

from .models import FacilityApplication


class FacilityApplicationForm(ModelForm):
    class Meta:
        model = FacilityApplication
        fields = [
            'alias', 'start', 'end', 'reason',
        ]
