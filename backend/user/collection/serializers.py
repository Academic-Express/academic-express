from typing import Any

from drf_spectacular.utils import (PolymorphicProxySerializer,
                                   extend_schema_field)
from rest_framework import serializers

from pub.models import ArxivEntry, GithubRepo
from pub.serializers import ArxivEntrySerializer, GithubRepoSerializer

from .models import Collection, CollectionGroup


class CollectionItemSerializer(serializers.Serializer):
    """
    收藏项，可以是 arXiv 论文或 GitHub 仓库。
    """
    type = serializers.ChoiceField(choices=['arxiv', 'github'])
    item = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField()

    @extend_schema_field(PolymorphicProxySerializer(
        component_name='CollectionItem',
        serializers=[
            ArxivEntrySerializer,
            GithubRepoSerializer,
        ],
        resource_type_field_name=None,
    ))
    def get_item(self, obj: dict[str, Any]):
        match obj['type']:
            case 'arxiv':
                return ArxivEntrySerializer(obj['item']).data
            case 'github':
                return GithubRepoSerializer(obj['item']).data


class CollectionSerializer(serializers.ModelSerializer):
    """收藏项序列化器"""
    item = serializers.SerializerMethodField()

    class Meta:
        model = Collection
        fields = ['id', 'item_type', 'item_id', 'created_at', 'item']
        read_only_fields = ['id', 'created_at']

    def get_item(self, obj):
        if obj.item_type == 'arxiv':
            try:
                entry = ArxivEntry.objects.get(arxiv_id=obj.item_id)
                return ArxivEntrySerializer(entry).data
            except ArxivEntry.DoesNotExist:
                return None
        elif obj.item_type == 'github':
            try:
                repo = GithubRepo.objects.get(repo_id=obj.item_id)
                return GithubRepoSerializer(repo).data
            except GithubRepo.DoesNotExist:
                return None
        return None


class CollectionGroupSerializer(serializers.ModelSerializer):
    """收藏分组序列化器"""
    items = CollectionSerializer(source='collections', many=True, read_only=True)
    items_count = serializers.SerializerMethodField()

    class Meta:
        model = CollectionGroup
        fields = ['id', 'name', 'description', 'is_public',
                  'created_at', 'updated_at', 'items', 'items_count']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_items_count(self, obj):
        return obj.collections.count()


class CollectionGroupManageItemsSerializer(serializers.Serializer):
    """管理收藏分组的序列化器"""
    action = serializers.ChoiceField(choices=['add', 'remove'])
    collection_ids = serializers.ListField(child=serializers.IntegerField())
