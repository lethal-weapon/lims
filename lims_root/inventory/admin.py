from django.contrib import admin

from .models import Apparatus, Laboratory


class ApparatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'model_no', 'cost', 'purchased', 'school', 'staff',)
    list_filter = ('school',)
    ordering = ('name',)
    search_fields = ('name', 'model_no',)
    exclude = ('staff',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Only set author during the first save.
            obj.staff = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        return self.permission_control(request, obj)

    def has_delete_permission(self, request, obj=None):
        return self.permission_control(request, obj)

    def permission_control(self, request, obj=None):
        if obj and obj.staff == request.user:
            return True
        return False


class LaboratoryAdmin(ApparatusAdmin):
    list_display = ('name', 'location', 'capacity', 'school', 'staff',)
    search_fields = ('name', 'location',)


admin.site.register(Apparatus, ApparatusAdmin)
admin.site.register(Laboratory, LaboratoryAdmin)
