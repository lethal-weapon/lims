from django.contrib import admin

from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('published', 'subject', 'content',)
    readonly_fields = ('published',)
    ordering = ('published',)
    search_fields = ('subject', 'content',)


admin.site.register(Article, ArticleAdmin)
