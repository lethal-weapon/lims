from django.contrib import admin

from .models import Article, FacilitySchedule


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('author', 'published', 'subject',)
    readonly_fields = ('published',)
    ordering = ('-published',)
    search_fields = ('subject', 'content',)
    exclude = ('author',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Only set author during the first save.
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        return self.permission_control(request, obj)

    def has_delete_permission(self, request, obj=None):
        return self.permission_control(request, obj)

    def permission_control(self, request, obj=None):
        if obj and obj.author == request.user:
            return True
        return False


class FacilityScheduleAdmin(admin.ModelAdmin):
    list_display = ('day', 'school', 'site', 'start', 'end',)
    list_filter = ('school',)
    ordering = ('-day',)
    search_fields = ('site',)
    exclude = ('creator',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Only set creator during the first save.
            obj.creator = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        return self.permission_control(request, obj)

    def has_delete_permission(self, request, obj=None):
        return self.permission_control(request, obj)

    def permission_control(self, request, obj=None):
        if obj and obj.creator == request.user:
            return True
        return False


admin.site.register(Article, ArticleAdmin)
admin.site.register(FacilitySchedule, FacilityScheduleAdmin)
