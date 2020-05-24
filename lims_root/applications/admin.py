from django.contrib import admin
from django.core.checks import messages

from inventory.models import Apparatus, Laboratory
from .models import FacilityApplication, ResearchApplication


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('applied_at', 'start', 'end', 'status', 'applicant',)
    list_filter = ('status',)
    ordering = ('-applied_at', 'start',)
    date_hierarchy = 'start'
    list_per_page = 10

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        # each staff only need to handle those applications
        # they are responsible for, which are defined as changeable
        ids = set()
        for app in qs:
            if self.has_change_permission(request, app):
                ids.add(app.id)

        return qs.filter(id__in=ids).exclude(status='PEN')

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.applicant == request.user:
            return True
        return False

    # Only set applicant field during the first save.
    # This is not intended for workers to create an application
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.applicant = request.user
        super().save_model(request, obj, form, change)

    def show_action_fail_message(self, request):
        self.message_user(request, level=messages.ERROR,
                          message='THE ACTION FAILED ON SOME INSTANCES!')

    # Additional actions for workers
    def approve_application(self, request, queryset):
        for obj in queryset:
            if self.has_change_permission(request, obj):
                queryset.update(status='WAI')
                queryset.update(reply='Your application has been approved. '
                                      'Remember to check the schedule in bulletin.')

    def decline_application(self, request, queryset):
        for obj in queryset:
            if self.has_change_permission(request, obj):
                queryset.update(status='CLO')
                queryset.update(reply='Your application has been declined.')

    def miss_facility_schedule(self, request, queryset):
        for obj in queryset:
            if self.has_change_permission(request, obj):
                queryset.update(status='CLO')
                queryset.update(reply='You missed the schedule! '
                                      'You have to apply it again if you still want it.')

    def mark_overtime(self, request, queryset):
        for obj in queryset:
            if self.has_change_permission(request, obj):
                queryset.update(status='OVE')
                queryset.update(reply='Your application has exceeded the promised time! '
                                      'FIRST WARNING!')

    def mark_facility_taken(self, request, queryset):
        for obj in queryset:
            if self.has_change_permission(request, obj):
                queryset.update(status='BOR')
                queryset.update(reply='You has borrowed the facilities successfully. '
                                      'Have fun with that!')

    def mark_facility_return(self, request, queryset):
        for obj in queryset:
            if self.has_change_permission(request, obj):
                queryset.update(status='CLO')
                queryset.update(reply='You has returned the facilities. Thank you!')


class FacilityApplicationAdmin(ApplicationAdmin):
    list_display = ('applied_at', 'start', 'end',
                    'status', 'applicant', 'items_display',)
    readonly_fields = ('applied_at', 'created_at', 'reason',
                       'applicant', 'items',)
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
        apparatus_ids = [apparatus.id for apparatus in Apparatus.objects.all()]
        item_names = []

        for item in obj.items.all():
            if item.id in apparatus_ids:
                item_names.append(Apparatus.objects.get(id=item.id).__str__())
            else:
                item_names.append(Laboratory.objects.get(id=item.id).__str__())

        return ", ".join(item_names)

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
    search_fields = ('title',)
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
    # that submitted by the people who come from his/her own school
    def has_change_permission(self, request, obj=None):
        if obj and obj.applicant.school == request.user.school:
            return True
        return False

    def approve_application(self, request, queryset):
        is_success = True
        for obj in queryset:
            if self.has_change_permission(request, obj):
                queryset.update(status='ONG')
                queryset.update(reply='Your research has been approved. Good Luck!')
            else:
                is_success = False
        if not is_success:
            self.show_action_fail_message(request)


admin.site.register(FacilityApplication, FacilityApplicationAdmin)
admin.site.register(ResearchApplication, ResearchApplicationAdmin)
