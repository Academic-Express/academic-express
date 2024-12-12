from datetime import datetime
from typing import TypedDict, Union

from django.utils.timezone import now, timedelta
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from pub.models import ArxivEntry, GithubRepo
from pub.utils import normalize_author
from sub.models import ScholarSubscription, TopicSubscription
from utils.exceptions import ErrorSerializer
from utils.feed_engine import session

from .serializers import (FollowFeedSerializer, HotFeedSerializer,
                          SubscriptionFeedSerializer)


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


class SubscriptionSource(TypedDict):
    topics: list[str]


class SubscriptionCandidate(TypedDict):
    origin: str
    item: Union[ArxivEntry, GithubRepo]
    timestamp: datetime
    source: SubscriptionSource

    _score: float


class ArxivSubscriptionCandidate(TypedDict):
    arxiv_id: str
    topic_scores: dict[str, float]


class GithubSubscriptionCandidate(TypedDict):
    full_name: str
    topic_scores: dict[str, float]


@extend_schema(
    operation_id='get_subscription_feed',
    responses={
        200: OpenApiResponse(
            SubscriptionFeedSerializer(many=True),
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
    user = request.user
    subscribed_topics: list[str] = []
    if user.is_authenticated:
        # 获取用户订阅的话题。
        subscribed_topics.extend(
            TopicSubscription.objects
            .filter(subscriber=user)
            .values_list('topic', flat=True)
        )

    if not subscribed_topics:
        # TODO: 从话题推荐模型中获取推荐的话题。
        subscribed_topics = ['Machine Learning', 'Computer Vision', 'Natural Language Processing']

    search_payload = {
        'queries': subscribed_topics,
        'max_results': 10,
    }

    candidates: list[SubscriptionCandidate] = []

    # 从推荐后端中获取推荐的 arXiv 论文。
    response = session.post('/arxiv/search', json=search_payload)
    response.raise_for_status()
    search_results = response.json()

    arxiv_candidates: dict[str, ArxivSubscriptionCandidate] = {}

    for topic, search_result in zip(subscribed_topics, search_results):
        for entry in search_result:
            candidate = arxiv_candidates.setdefault(entry['entry_id'], {
                'arxiv_id': entry['entry_id'],
                'topic_scores': {},
            })
            candidate['topic_scores'][topic] = entry['score']

    for candidate in arxiv_candidates.values():
        try:
            arxiv_entry = ArxivEntry.objects.get(arxiv_id=candidate['arxiv_id'])
        except ArxivEntry.DoesNotExist:
            continue

        score = get_arxiv_subscription_score(candidate, arxiv_entry)

        candidates.append({
            'origin': 'arxiv',
            'item': arxiv_entry,
            'timestamp': arxiv_entry.published,
            'source': {
                'topics': list_top_topics(candidate['topic_scores']),
            },
            '_score': score,
        })

    # 从推荐后端中获取推荐的 GitHub 仓库。
    response = session.post('/github/search', json=search_payload)
    response.raise_for_status()
    search_results = response.json()

    github_candidates: dict[str, GithubSubscriptionCandidate] = {}

    for topic, search_result in zip(subscribed_topics, search_results):
        for entry in search_result:
            candidate = github_candidates.setdefault(entry['entry_id'], {
                'full_name': entry['entry_id'],
                'topic_scores': {},
            })
            candidate['topic_scores'][topic] = entry['score']

    for candidate in github_candidates.values():
        try:
            github_repo = GithubRepo.objects.get(full_name=candidate['full_name'])
        except GithubRepo.DoesNotExist:
            continue

        score = get_github_subscription_score(candidate, github_repo)

        candidates.append({
            'origin': 'github',
            'item': github_repo,
            'timestamp': github_repo.pushed_at,
            'source': {
                'topics': list_top_topics(candidate['topic_scores']),
            },
            '_score': score,
        })

    # 按得分排序候选集。
    sorted_candidates = sorted(
        candidates,
        key=lambda candidate: candidate['_score'],
        reverse=True,
    )
    sorted_candidates = sorted_candidates[:50]

    return Response(SubscriptionFeedSerializer(sorted_candidates, many=True).data)


def get_arxiv_subscription_score(
    candidate: ArxivSubscriptionCandidate,
    arxiv_entry: ArxivEntry,
) -> float:
    """
    计算 arXiv 论文的订阅推荐得分。
    """
    # 计算话题相似度得分。
    overall_topic_score = sum(candidate['topic_scores'].values())

    # 计算时效性得分。
    elapsed_days = (now() - arxiv_entry.published).days
    freshness_score = 1 / (1 + elapsed_days)

    return 0.5 * overall_topic_score + 0.5 * freshness_score


def get_github_subscription_score(
    candidate: GithubSubscriptionCandidate,
    github_repo: GithubRepo,
) -> float:
    """
    计算 GitHub 仓库的订阅推荐得分。
    """
    # 计算话题相似度得分。
    sum_topic_scores = sum(candidate['topic_scores'].values())
    num_topics = len(candidate['topic_scores'])
    overall_topic_score = sum_topic_scores / (1 + num_topics) ** 0.5

    # 计算时效性得分。
    created_days = (now() - github_repo.created_at).days
    pushed_days = (now() - github_repo.pushed_at).days
    freshness_score = 0.5 / (1 + pushed_days) + 0.5 / (1 + created_days)

    return 0.5 * overall_topic_score + 0.5 * freshness_score


def list_top_topics(topic_scores: dict[str, float], top_n: int = 3) -> list[str]:
    """
    列出得分最高的话题。
    """
    return sorted(
        topic_scores.keys(),
        key=lambda topic: topic_scores[topic],
        reverse=True,
    )[:top_n]


class HotCandidate(TypedDict):
    origin: str
    item: Union[ArxivEntry, GithubRepo]
    timestamp: datetime

    _score: float


@extend_schema(
    operation_id='get_hot_feed',
    responses={
        200: OpenApiResponse(
            HotFeedSerializer(many=True),
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
    # 获取最近 30 天的 arXiv 论文和 GitHub 仓库。
    one_week_ago = now() - timedelta(days=30)
    arxiv_entries = ArxivEntry.objects.filter(published__gte=one_week_ago, view_count__gt=0)
    github_repos = GithubRepo.objects.filter(pushed_at__gte=one_week_ago, view_count__gt=0)

    # 计算热点追踪得分。
    arxiv_candidates: list[HotCandidate] = []
    for entry in arxiv_entries:
        score = get_arxiv_hot_score(entry)
        arxiv_candidates.append({
            'origin': 'arxiv',
            'item': entry,
            'timestamp': entry.published,
            '_score': score,
        })

    github_candidates: list[HotCandidate] = []
    for repo in github_repos:
        score = get_github_hot_score(repo)
        github_candidates.append({
            'origin': 'github',
            'item': repo,
            'timestamp': repo.pushed_at,
            '_score': score,
        })

    # 分别标准化两个集合的得分。
    normalize_hot_scores(arxiv_candidates)
    normalize_hot_scores(github_candidates)

    # 按得分排序候选集。
    candidates = arxiv_candidates + github_candidates
    candidates.sort(key=lambda candidate: candidate['_score'], reverse=True)

    # 选取得分最高的 50 个候选。
    candidates = candidates[:50]

    return Response(HotFeedSerializer(candidates, many=True).data)


def get_arxiv_hot_score(arxiv_entry: ArxivEntry) -> float:
    """
    计算 arXiv 论文的热点追踪得分。
    """
    # 计算浏览次数得分。
    view_count = arxiv_entry.view_count

    # 计算时效性得分。
    elapsed_days = (now() - arxiv_entry.published).days
    freshness_score = 1 / (1 + elapsed_days) ** 0.4

    return view_count * freshness_score


def get_github_hot_score(github_repo: GithubRepo) -> float:
    """
    计算 GitHub 仓库的热点追踪得分。
    """
    # 计算浏览次数得分。
    view_count = github_repo.view_count

    # 计算时效性得分。
    created_days = (now() - github_repo.created_at).days
    pushed_days = (now() - github_repo.pushed_at).days
    freshness_score = 0.5 / (1 + pushed_days) ** 0.5 + 0.5 / (1 + created_days) ** 0.3

    return view_count * freshness_score


def normalize_hot_scores(candidates: list[HotCandidate]) -> None:
    """
    标准化热点追踪得分。
    """
    if not candidates:
        return

    scores = [candidate['_score'] for candidate in candidates]
    mean_score = sum(scores) / len(scores)
    std_score = (sum((score - mean_score) ** 2 for score in scores) / len(scores)) ** 0.5 + 1e-6

    for candidate in candidates:
        candidate['_score'] = (candidate['_score'] - mean_score) / std_score
