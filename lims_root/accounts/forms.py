from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from .models import Account


class RegistrationForm(UserCreationForm):
    campus_id = forms.CharField(max_length=30)

    class Meta:
        model = Account
        fields = ('email', 'campus_id', 'password1', 'password2',)


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('campus_id', 'password')

    def clean(self):
        if self.is_valid():
            campus_id = self.cleaned_data['campus_id']
            password = self.cleaned_data['password']
            if not authenticate(campus_id=campus_id, password=password):
                raise forms.ValidationError("Invalid Credentials")


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            account = Account.objects \
                .exclude(pk=self.instance.pk) \
                .get(email__iexact=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % email)


class AccountImportForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = (
            'id', 'password', 'email', 'campus_id',
            'name', 'school', 'limit',
            'role', 'is_active', 'is_verified',
        )


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()
