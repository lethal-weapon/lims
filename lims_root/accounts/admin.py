from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.core.checks import messages
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


# The base admin is able to import/export model data in CSV
class MyBaseModelAdmin(admin.ModelAdmin, ExportCsvMixin, ImportCsvMixin):
    change_list_template = 'lims_site/my-admin-changelist.html'
    actions = ('export_as_csv',)
    model_import_form = forms.ModelForm

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == 'GET':
            return render(request, 'lims_site/csv-form.html', {
                'form': CsvImportForm()
            })

        elif request.method == 'POST':
            self.import_as_csv(
                csv_file=request.FILES['csv_file'],
                model_form=self.model_import_form)
            self.message_user(request, 'Your csv file has been imported')
            return redirect('..')


class AccountAdmin(UserAdmin, MyBaseModelAdmin):
    # The forms to add/change/import user instances
    form = UserChangeForm
    add_form = UserCreationForm
    model_import_form = AccountImportForm

    list_display = ('campus_id', 'name', 'school',
                    'email', 'role', 'is_verified',)
    list_filter = ('is_verified', 'school', 'role',)
    search_fields = ('campus_id', 'name', 'email',)
    readonly_fields = ('last_login', 'date_joined',)
    ordering = ('campus_id',)
    actions = ('export_as_csv', 'mark_verified_student',
               'mark_verified_teacher', 'mark_outdated_user',)
    filter_horizontal = ()
    list_per_page = 25

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

    # def delete_model(self, request, obj):
    # def delete_queryset(self, request, queryset):

    # save is one kind of change too
    def save_model(self, request, obj, form, change):
        if self.permission_control(request, obj):
            super().save_model(request, obj, form, change)
        else:
            self.message_user(request, level=messages.ERROR, message='PERMISSION DENIED')

    def has_view_permission(self, request, obj=None):
        return request.user.role == 'SUP' or \
               request.user.role == 'ADM'

    def has_add_permission(self, request):
        return request.user.role == 'SUP' or \
               request.user.role == 'ADM'

    def has_change_permission(self, request, obj=None):
        return self.permission_control(request, obj)

    def has_delete_permission(self, request, obj=None):
        return self.permission_control(request, obj)

    def permission_control(self, request, obj=None):
        if request.user.role == 'SUP':
            return True
        elif request.user.role == 'ADM':
            if obj is None:
                return True
            elif obj and obj.role != 'ADM' and obj.role != 'SUP':
                return True
        return False

    # Additional actions for admins
    def mark_verified_student(self, request, queryset):
        for obj in queryset:
            if self.has_change_permission(request, obj):
                queryset.update(role='STU', limit=3, is_verified=True)

    def mark_verified_teacher(self, request, queryset):
        for obj in queryset:
            if self.has_change_permission(request, obj):
                queryset.update(role='TEA', limit=5, is_verified=True)

    def mark_outdated_user(self, request, queryset):
        for obj in queryset:
            if self.has_change_permission(request, obj):
                queryset.update(is_active=False, is_verified=False)


admin.site.register(Account, AccountAdmin)
# since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
