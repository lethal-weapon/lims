from django.contrib import admin

from accounts.admin import MyBaseModelAdmin
from .forms import ArticleImportForm, FacilityScheduleImportForm
from .models import Article, FacilitySchedule


class ArticleAdmin(MyBaseModelAdmin):
    list_display = ('author', 'published', 'subject',)
    readonly_fields = ('published',)
    ordering = ('-published', 'author',)
    search_fields = ('subject', 'content',)
    exclude = ('author',)
    date_hierarchy = 'published'
    list_per_page = 15
    model_import_form = ArticleImportForm

    # Only set author field during the first save.
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        return self.permission_control(request, obj)

    def has_delete_permission(self, request, obj=None):
        if request.user.role == 'SUP':
            return True
        return self.permission_control(request, obj)

    def permission_control(self, request, obj=None):
        if obj and obj.author == request.user:
            return True
        return False


class FacilityScheduleAdmin(MyBaseModelAdmin):
    list_display = ('day', 'start', 'end', 'site', 'school',)
    list_filter = ('school',)
    ordering = ('-day', 'start',)
    search_fields = ('site',)
    exclude = ('creator',)
    date_hierarchy = 'day'
    list_per_page = 25
    model_import_form = FacilityScheduleImportForm

    # Only set creator field during the first save.
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creator = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        return self.permission_control(request, obj)

    def has_delete_permission(self, request, obj=None):
        if request.user.role == 'SUP':
            return True
        return self.permission_control(request, obj)

    def permission_control(self, request, obj=None):
        if obj and obj.creator == request.user:
            return True
        return False


admin.site.register(Article, ArticleAdmin)
admin.site.register(FacilitySchedule, FacilityScheduleAdmin)
