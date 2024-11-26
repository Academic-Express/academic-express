from datetime import datetime
from typing import TypedDict, Union

from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from pub.models import ArxivEntry, GithubRepo
from pub.utils import normalize_author
from sub.models import ScholarSubscription
from utils.exceptions import ErrorSerializer

from .serializers import FollowFeedSerializer


class FollowSource(TypedDict):
    scholar_names: list[str]


class FollowCandidate(TypedDict):
    origin: str
    item: Union[ArxivEntry, GithubRepo]
    timestamp: datetime
    source: FollowSource


@extend_schema(
    operation_id='get_follow_feed',
    responses={
        200: OpenApiResponse(
            FollowFeedSerializer(many=True),
            description='获取关注动态成功',
        ),
        401: OpenApiResponse(ErrorSerializer, description='未登录'),
    },
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_follow_feed(request: Request):
    """
    获取关注动态。
    """
    # 获取用户关注的学者。
    followed_scholar_names = (
        ScholarSubscription.objects
        .filter(subscriber=request.user)
        .values_list('scholar_name', flat=True)
    )

    candidates: list[FollowCandidate] = []
    candidate_arxiv_entries: dict[str, FollowCandidate] = {}

    for scholar_name in followed_scholar_names:
        # 召回学者的最新论文。
        normalized = normalize_author(scholar_name)
        arxiv_entries = ArxivEntry.objects.filter(
            arxiventryauthor__first_name=normalized['first_name'],
            arxiventryauthor__last_name=normalized['last_name'],
        ).order_by('-published')[:10]

        for entry in arxiv_entries:
            # 检查论文是否已经在其他学者的动态中。
            if candidate := candidate_arxiv_entries.get(entry.arxiv_id):
                candidate['source']['scholar_names'].append(scholar_name)
                continue

            # 将论文加入候选集。
            candidate = {
                'origin': 'arxiv',
                'item': entry,
                'timestamp': entry.published,
                'source': {
                    'scholar_names': [scholar_name],
                },
            }
            candidates.append(candidate)
            candidate_arxiv_entries[entry.arxiv_id] = candidate

    # 按时间顺序排序候选集。
    sorted_candidates = sorted(
        candidate_arxiv_entries.values(),
        key=lambda candidate: candidate['timestamp'],
        reverse=True,
    )

    return Response(FollowFeedSerializer(sorted_candidates, many=True).data)


@extend_schema(
    operation_id='get_subscription_feed',
    responses={
        200: OpenApiResponse(
            NotImplemented,
            description='获取订阅推荐成功',
        ),
    },
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_subscription_feed(request: Request):
    """
    获取订阅推荐。
    """
    return Response(status=status.HTTP_501_NOT_IMPLEMENTED)


@extend_schema(
    operation_id='get_hot_feed',
    responses={
        200: OpenApiResponse(
            NotImplemented,
            description='获取热点追踪成功',
        ),
    },
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_hot_feed(request: Request):
    """
    获取热点追踪。
    """
    return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
