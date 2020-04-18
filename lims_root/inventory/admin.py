from django.contrib import admin

from .models import Apparatus, Laboratory


class ApparatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'model_no', 'cost', 'purchased', 'school', 'staff',)
    list_filter = ('school',)
    ordering = ('name',)
    search_fields = ('name', 'model_no',)


class LaboratoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'capacity', 'school', 'staff',)
    list_filter = ('school',)
    ordering = ('name',)
    search_fields = ('name', 'location',)


admin.site.register(Apparatus, ApparatusAdmin)
admin.site.register(Laboratory, LaboratoryAdmin)
