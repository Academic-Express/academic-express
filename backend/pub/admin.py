from django.contrib import admin

from .models import ArxivEntry, GithubRepo


class ArxivEntryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('arxiv_id', 'title', 'primary_category', 'published_date', 'updated_date')
    search_fields = ('arxiv_id', 'title', 'summary')
    list_filter = ('primary_category', 'published_date', 'updated_date')


class GithubRepoAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'description', 'language', 'created_at', 'updated_at')
    search_fields = ('name', 'full_name', 'description')
    list_filter = ('language', 'created_at', 'updated_at')


admin.site.register(ArxivEntry)
admin.site.register(GithubRepo)
