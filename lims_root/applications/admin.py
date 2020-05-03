from django.contrib import admin

from .models import FacilityApplication, ResearchApplication


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('applied_at', 'start', 'end', 'status', 'applicant',)
    list_filter = ('status',)
    ordering = ('applied_at', 'start',)
    search_fields = ('applicant',)
    readonly_fields = ('applied_at', 'created_at', 'reason', 'applicant',)
    list_per_page = 10
    date_hierarchy = 'start'

    def has_delete_permission(self, request, obj=None):
        if obj and obj.applicant == request.user:
            return True
        return False

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Only set applicant during the first save.
            obj.applicant = request.user
        super().save_model(request, obj, form, change)

    def approve_application(self, request, queryset):
        queryset.update(status='WAI')

    def decline_application(self, request, queryset):
        queryset.update(status='CLO')

    def miss_facility_schedule(self, request, queryset):
        queryset.update(status='CLO')

    def mark_overtime(self, request, queryset):
        queryset.update(status='OVE')

    def mark_facility_taken(self, request, queryset):
        queryset.update(status='BOR')

    def mark_facility_return(self, request, queryset):
        queryset.update(status='CLO')


class FacilityApplicationAdmin(ApplicationAdmin):
    list_display = ('applied_at', 'start', 'end',
                    'status', 'applicant', 'items_display',)
    actions = ('approve_application', 'decline_application',
               'miss_facility_schedule', 'mark_overtime',
               'mark_facility_taken', 'mark_facility_return',)
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

    def items_display(self, obj):
        return ", ".join([
            item.name for item in obj.items.all()
        ])

    items_display.short_description = "Items"

    # each staff should only manage those facility applications
    # whose applied items are managed by staff himself/herself
    def has_change_permission(self, request, obj=None):
        if obj:
            for item in obj.items.all():
                if item.staff == request.user:
                    return True
        return False


class ResearchApplicationAdmin(ApplicationAdmin):
    search_fields = ('title', 'applicant', 'members',)
    readonly_fields = ('applied_at', 'created_at', 'reason',
                       'applicant', 'members', 'title',)
    actions = ('approve_application', 'decline_application', 'mark_overtime',)
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

    # each staff should only manage those research applications
    # that submitted by the people who come from his/her school
    def has_change_permission(self, request, obj=None):
        if obj and obj.applicant.school == request.user.school:
            return True
        return False

    def approve_application(self, request, queryset):
        queryset.update(status='ONG')


admin.site.register(FacilityApplication, FacilityApplicationAdmin)
admin.site.register(ResearchApplication, ResearchApplicationAdmin)
