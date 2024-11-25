from django.contrib import admin

from .models import ScholarSubscription, TopicSubscription


class TopicSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['subscriber', 'topic', 'created_at', 'updated_at']
    search_fields = ['subscriber', 'topic']
    list_filter = ['created_at', 'updated_at']


class ScholarSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['subscriber', 'scholar_name', 'created_at', 'updated_at']
    search_fields = ['subscriber', 'scholar_name']
    list_filter = ['created_at', 'updated_at']


admin.site.register(TopicSubscription, TopicSubscriptionAdmin)
admin.site.register(ScholarSubscription, ScholarSubscriptionAdmin)
