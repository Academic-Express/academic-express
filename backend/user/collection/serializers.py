from typing import Any

from drf_spectacular.utils import (PolymorphicProxySerializer,
                                   extend_schema_field)
from rest_framework import serializers

from pub.serializers import ArxivEntrySerializer, GithubRepoSerializer
from .models import Collection, CollectionItem


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
    """
    收藏夹
    """
    items = serializers.SerializerMethodField()

    class Meta:
        model = Collection
        fields = ['id', 'name', 'description', 'is_public',
                  'created_at', 'updated_at', 'items']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_items(self, obj):
        items = []
        # 获取 ArXiv 论文收藏
        arxiv_items = obj.collectionarxiventry_set.all()
        for item in arxiv_items:
            items.append({
                'type': 'arxiv',
                'item': ArxivEntrySerializer(item.entry).data,
                'created_at': item.collection_time
            })

        # 获取 GitHub 仓库收藏
        github_items = obj.collectiongithubrepo_set.all()
        for item in github_items:
            items.append({
                'type': 'github',
                'item': GithubRepoSerializer(item.repo).data,
                'created_at': item.collection_time
            })

        # 按收藏时间排序
        items.sort(key=lambda x: x['created_at'], reverse=True)
        return items
