from django.contrib import admin

from .models import Comment, Vote


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'resource', 'content', 'parent', 'created_at')
    list_filter = ('author', 'resource', 'created_at')
    search_fields = ('content',)


class VoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'comment', 'value', 'created_at')
    list_filter = ('user', 'comment', 'value', 'created_at')
    search_fields = ('user',)


admin.site.register(Comment, CommentAdmin)
admin.site.register(Vote, VoteAdmin)
