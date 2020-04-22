from django.contrib import admin

from .models import Article, FacilitySchedule


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('published', 'subject', 'content',)
    readonly_fields = ('published',)
    ordering = ('-published',)
    search_fields = ('subject', 'content',)


class FacilityScheduleAdmin(admin.ModelAdmin):
    list_display = ('day', 'school', 'site', 'start', 'end',)
    list_filter = ('school',)
    ordering = ('-day',)
    search_fields = ('site', )


admin.site.register(Article, ArticleAdmin)
admin.site.register(FacilitySchedule, FacilityScheduleAdmin)
