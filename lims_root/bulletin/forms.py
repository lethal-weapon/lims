from django import forms

from .models import Article, FacilitySchedule


class ArticleImportForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = (
            'id', 'subject', 'content', 'author',
        )


class FacilityScheduleImportForm(forms.ModelForm):
    class Meta:
        model = FacilitySchedule
        fields = (
            'id', 'school', 'site',
            'day', 'start', 'end', 'creator',
        )
