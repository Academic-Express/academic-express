from typing import Any

from drf_spectacular.utils import (PolymorphicProxySerializer,
                                   extend_schema_field)
from rest_framework import serializers

from pub.serializers import ArxivEntrySerializer, GithubRepoSerializer


class FeedSerializer(serializers.Serializer):
    """
    推送的动态，可以是 arXiv 论文或 GitHub 仓库。
    """
    origin = serializers.ChoiceField(choices=['arxiv', 'github'])
    item = serializers.SerializerMethodField()
    timestamp = serializers.DateTimeField()

    @extend_schema_field(PolymorphicProxySerializer(
        component_name='FeedItem',
        serializers=[
            ArxivEntrySerializer,
            GithubRepoSerializer,
        ],
        resource_type_field_name=None,
    ))
    def get_item(self, obj: dict[str, Any]):
        match obj['origin']:
            case 'arxiv':
                return ArxivEntrySerializer(obj['item']).data
            case 'github':
                return GithubRepoSerializer(obj['item']).data


class FollowSourceSerializer(serializers.Serializer):
    """
    关注来源，目前只支持学者。
    """
    scholar_names = serializers.ListField(child=serializers.CharField(), required=False)


class FollowFeedSerializer(FeedSerializer):
    """
    关注动态。
    """
    source = FollowSourceSerializer()


class SubscriptionSourceSerializer(serializers.Serializer):
    """
    订阅来源，目前只支持话题。
    """
    topics = serializers.ListField(child=serializers.CharField(), required=False)


class SubscriptionFeedSerializer(FeedSerializer):
    """
    订阅推荐。
    """
    source = SubscriptionSourceSerializer()


class HotFeedSerializer(FeedSerializer):
    """
    热门动态。
    """
