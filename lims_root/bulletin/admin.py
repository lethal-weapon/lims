from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from accounts.admin import MyBaseModelAdmin
from .forms import ArticleImportForm, FacilityScheduleImportForm
from .models import Article, FacilitySchedule


class AuthorFilter(SimpleListFilter):
    title = 'author'
    parameter_name = 'author'

    def lookups(self, request, model_admin):
        authors = set([a.author for a in model_admin.model.objects.all()])
        return [(a.id, a.name) for a in authors]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(author__id__exact=self.value())


class ArticleAdmin(MyBaseModelAdmin):
    list_display = ('author', 'published', 'subject',)
    list_filter = (AuthorFilter,)
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
        return self.permission_control(request, obj)

    def permission_control(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.author == request.user:
            return True
        return False


class CreatorFilter(SimpleListFilter):
    title = 'creator'
    parameter_name = 'creator'

    def lookups(self, request, model_admin):
        creators = set([fs.creator for fs in model_admin.model.objects.all()])
        return [(c.id, c.name) for c in creators]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(creator__id__exact=self.value())


class FacilityScheduleAdmin(MyBaseModelAdmin):
    list_display = ('day', 'start', 'end', 'site', 'school', 'creator',)
    list_filter = ('school', CreatorFilter,)
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
        return self.permission_control(request, obj)

    def permission_control(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.creator == request.user:
            return True
        return False


admin.site.register(Article, ArticleAdmin)
admin.site.register(FacilitySchedule, FacilityScheduleAdmin)
