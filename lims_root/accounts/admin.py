from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render
from django.urls import path

from .forms import AccountImportForm, CsvImportForm
from .mixins import ExportCsvMixin, ImportCsvMixin
from .models import Account


# A form for creating users
# Includes all the required fields, plus a repeated password
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('campus_id', 'email',)

    # Check if the two password entries match
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    # Save the provided password in hashed format
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


# A form for updating users
# Includes all the fields on the user, but replaces
# the password field with admin's password hash display field
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Account
        fields = ('email', 'campus_id', 'password',
                  'name', 'school', 'limit',
                  'role', 'is_active', 'is_verified',)

    # Regardless of what the user provides, return the initial value.
    # This is done here, rather than on the field, because the
    # field does not have access to the initial value
    def clean_password(self):
        return self.initial['password']


class AccountAdmin(UserAdmin, ExportCsvMixin, ImportCsvMixin):
    change_list_template = 'accounts/accounts_changelist.html'

    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('campus_id', 'name', 'school',
                    'email', 'role', 'is_verified',)
    list_filter = ('is_verified', 'school', 'role',)
    search_fields = ('campus_id', 'name', 'email',)
    readonly_fields = ('last_login', 'date_joined',)
    ordering = ('campus_id',)
    actions = ('export_as_csv', 'mark_verified_student',
               'mark_verified_teacher', 'mark_outdated_user',)
    filter_horizontal = ()

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    fieldsets = (
        ('Basics', {
            'fields': ('campus_id', 'password',)
        }),
        ('Personal info', {
            'fields': ('name', 'school', 'email', 'limit',)
        }),
        ('Role status', {
            'fields': ('role', 'is_active', 'is_verified',)
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined',)
        }),
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        ('Basics', {
            'classes': ('wide',),
            'fields' : ('campus_id', 'email', 'password1', 'password2'),
        }),
    )

    # Additional actions for admins
    def mark_verified_student(self, request, queryset):
        queryset.update(role='STU', limit=3, is_verified=True)

    def mark_verified_teacher(self, request, queryset):
        queryset.update(role='TEA', limit=5, is_verified=True)

    def mark_outdated_user(self, request, queryset):
        queryset.update(is_active=False, is_verified=False)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == 'GET':
            return render(request, 'accounts/csv_form.html', {
                'form': CsvImportForm()
            })

        elif request.method == 'POST':
            self.import_as_csv(
                csv_file=request.FILES['csv_file'],
                model_form=AccountImportForm)
            self.message_user(request, 'Your csv file has been imported')
            return redirect('..')


admin.site.register(Account, AccountAdmin)
# since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
