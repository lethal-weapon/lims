from django.contrib import admin

from .models import FacilityApplication, ResearchApplication


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('submitted', 'start', 'end', 'status', 'applicant',)
    list_filter = ('status',)
    ordering = ('submitted', 'start',)
    search_fields = ('applicant',)
    readonly_fields = ('submitted',)

    fieldsets = (
        ('Basics', {
            'fields': ('submitted', 'start', 'end', 'status',)
        }),
        ('Details', {
            'fields': ('reason', 'reply',)
        }),
        ('Applications', {
            'fields': ('applicant', 'items',)
        }),
    )


class ResearchApplicationAdmin(ApplicationAdmin):
    search_fields = ('applicant', 'title', 'members',)
    fieldsets = (
        ('Basics', {
            'fields': ('submitted', 'start', 'end', 'status',)
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
