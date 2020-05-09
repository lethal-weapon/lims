from django import forms

from .models import Apparatus, Laboratory


class ApparatusImportForm(forms.ModelForm):
    class Meta:
        model = Apparatus
        fields = (
            'id', 'name', 'staff', 'school',
            'cost', 'model_no', 'purchased',
        )


class LaboratoryImportForm(forms.ModelForm):
    class Meta:
        model = Laboratory
        fields = (
            'id', 'name', 'staff', 'school',
            'location', 'capacity',
        )
