from django.contrib import admin

from .models import FacilityApplication, ResearchApplication


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('applied_at', 'start', 'end', 'status', 'applicant',)
    list_filter = ('status',)
    ordering = ('applied_at', 'start',)
    search_fields = ('applicant',)
    readonly_fields = ('applied_at', 'created_at',)

    fieldsets = (
        ('Basics', {
            'fields': ('applied_at', 'start', 'end', 'status',)
        }),
        ('Details', {
            'fields': ('reason', 'reply',)
        }),
        ('Applications', {
            'fields': ('applicant', 'items',)
        }),
    )


class ResearchApplicationAdmin(ApplicationAdmin):
    search_fields = ('title', 'applicant', 'members',)
    fieldsets = (
        ('Basics', {
            'fields': ('applied_at', 'start', 'end', 'status',)
        }),
        ('Details', {
            'fields': ('reason', 'reply',)
        }),
        ('Applications', {
            'fields': ('title', 'applicant', 'members',)
        }),
    )


admin.site.register(FacilityApplication, ApplicationAdmin)
admin.site.register(ResearchApplication, ResearchApplicationAdmin)
