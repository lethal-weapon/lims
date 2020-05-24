from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from accounts.admin import MyBaseModelAdmin
from .forms import ApparatusImportForm, LaboratoryImportForm
from .models import Apparatus, Laboratory


class StaffFilter(SimpleListFilter):
    title = 'staff'
    parameter_name = 'staff'

    def lookups(self, request, model_admin):
        staffs = set([f.staff for f in model_admin.model.objects.all()])
        return [(s.id, s.name) for s in staffs]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(staff__id__exact=self.value())


class FacilityAdmin(MyBaseModelAdmin):
    list_filter = ('school', StaffFilter,)
    exclude = ('staff',)

    # Only set staff field during the first save.
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.staff = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        return self.permission_control(request, obj)

    def has_delete_permission(self, request, obj=None):
        return self.permission_control(request, obj)

    def permission_control(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.staff == request.user:
            return True
        return False


class ApparatusAdmin(FacilityAdmin):
    list_display = ('name', 'model_no', 'cost', 'purchased', 'school', 'staff',)
    ordering = ('name', 'model_no',)
    search_fields = ('name', 'model_no',)
    date_hierarchy = 'purchased'
    list_per_page = 50
    model_import_form = ApparatusImportForm


class LaboratoryAdmin(FacilityAdmin):
    list_display = ('name', 'location', 'capacity', 'school', 'staff',)
    ordering = ('school', 'location',)
    search_fields = ('name', 'location',)
    list_per_page = 25
    model_import_form = LaboratoryImportForm


admin.site.register(Apparatus, ApparatusAdmin)
admin.site.register(Laboratory, LaboratoryAdmin)
