from django.contrib import admin

from .models import ArxivEntry


class ArxivEntryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('arxiv_id', 'title', 'primary_category', 'published_date', 'updated_date')
    search_fields = ('arxiv_id', 'title', 'summary')
    list_filter = ('primary_category', 'published_date', 'updated_date')


admin.site.register(ArxivEntry)
