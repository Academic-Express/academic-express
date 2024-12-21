from django.contrib import admin

from .models import ArxivCategory, ArxivEntry, GithubRepo, ResourceClaim


class ArxivEntryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('arxiv_id', 'title', 'primary_category', 'published', 'updated')
    search_fields = ('arxiv_id', 'title', 'summary')
    list_filter = ('primary_category', 'published', 'updated')


class ArxivCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'name', 'description')
    search_fields = ('category_id', 'name', 'description')


class GithubRepoAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'description', 'language', 'created_at', 'updated_at')
    search_fields = ('name', 'full_name', 'description')
    list_filter = ('language', 'created_at', 'updated_at')


class ResourceClaimAdmin(admin.ModelAdmin):
    list_display = ('user', 'resource_type', 'resource_id', 'created_at')
    search_fields = ('user__username', 'resource_type', 'resource_id')
    list_filter = ('resource_type', 'created_at')


admin.site.register(ArxivEntry, ArxivEntryAdmin)
admin.site.register(ArxivCategory, ArxivCategoryAdmin)
admin.site.register(GithubRepo, GithubRepoAdmin)
admin.site.register(ResourceClaim, ResourceClaimAdmin)
