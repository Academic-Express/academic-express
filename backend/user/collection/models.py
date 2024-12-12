from django.conf import settings
from django.db import models


class Collection(models.Model):
    """单个收藏项"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item_type = models.CharField(max_length=10, choices=[
        ('arxiv', 'ArXiv Paper'),
        ('github', 'GitHub Repository'),
    ], default='arxiv')
    item_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '收藏项目'
        verbose_name_plural = '收藏项目'
        db_table = 'collection_item'
        unique_together = ('user', 'item_type', 'item_id')


class CollectionGroup(models.Model):
    """收藏分组"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    collections = models.ManyToManyField(Collection, through='GroupCollection')

    class Meta:
        verbose_name = '收藏分组'
        verbose_name_plural = '收藏分组'
        db_table = 'collection_group'
        unique_together = ('user', 'name')


class GroupCollection(models.Model):
    """分组与收藏的关联"""
    group = models.ForeignKey(CollectionGroup, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '收藏分组项目'
        verbose_name_plural = '收藏分组项目'
        db_table = 'collection_group_item'
        unique_together = ('group', 'collection')
