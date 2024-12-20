from django.db.models import F
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from history.utils import record_history
from utils.exceptions import ErrorSerializer

from .models import ArxivEntry, GithubRepo, ResourceClaim
from .serializers import (ArxivEntrySerializer, GithubRepoSerializer,
                          ResourceClaimSerializer)


@extend_schema(
    operation_id='get_arxiv_entry',
    responses={
        200: OpenApiResponse(ArxivEntrySerializer, description='获取 ArXiv 论文成功'),
        404: OpenApiResponse(ErrorSerializer, description='ArXiv 论文不存在'),
    },
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_arxiv_entry(request: Request, arxiv_id: str):
    """
    获取 ArXiv 论文。
    """
    try:
        entry = ArxivEntry.objects.get(arxiv_id=arxiv_id)
    except ArxivEntry.DoesNotExist:
        raise NotFound('ArXiv 论文不存在。')

    if request.user.is_authenticated:
        record_history(request.user, 'arxiv', entry)

    entry.view_count = F('view_count') + 1
    entry.save(update_fields=['view_count'])
    entry.refresh_from_db()

    serializer = ArxivEntrySerializer(entry)
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    operation_id='get_github_repo',
    responses={
        200: OpenApiResponse(GithubRepoSerializer, description='获取 Github 仓库成功'),
        404: OpenApiResponse(ErrorSerializer, description='Github 仓库不存在'),
    },
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_github_repo(request: Request, owner: str, repo_name: str):
    """
    获取 Github 仓库。
    """
    try:
        repo = GithubRepo.objects.get(full_name=f'{owner}/{repo_name}')
    except GithubRepo.DoesNotExist:
        raise NotFound('Github 仓库不存在。')

    if request.user.is_authenticated:
        record_history(request.user, 'github', repo)

    repo.view_count = F('view_count') + 1
    repo.save(update_fields=['view_count'])
    repo.refresh_from_db()

    serializer = GithubRepoSerializer(repo)
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    operation_id='get_resource_claims',
    responses={
        200: OpenApiResponse(
            response=ResourceClaimSerializer(many=True),
            description='获取资源认领列表成功'
        ),
        404: OpenApiResponse(
            response=ErrorSerializer,
            description='资源不存在'
        )
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_resource_claims(request: Request, resource: str, resource_id: str) -> Response:
    """
    获取资源的认领列表。
    """
    # 验证资源类型
    if resource not in ['arxiv', 'github']:
        raise NotFound('资源类型不存在。')

    # 验证资源是否存在
    if resource == 'arxiv':
        if not ArxivEntry.objects.filter(arxiv_id=resource_id).exists():
            raise NotFound('ArXiv 论文不存在。')
    else:  # github
        if not GithubRepo.objects.filter(repo_id=resource_id).exists():
            raise NotFound('GitHub 仓库不存在。')

    claims = ResourceClaim.objects.filter(
        resource_type=resource,
        resource_id=resource_id
    )
    serializer = ResourceClaimSerializer(claims, many=True)
    return Response(serializer.data)


@extend_schema(
    operation_id='toggle_resource_claim',
    request=None,
    responses={
        200: OpenApiResponse(
            response=ResourceClaimSerializer,
            description='认领/取消认领成功'
        ),
        404: OpenApiResponse(
            response=ErrorSerializer,
            description='资源不存在'
        )
    }
)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def toggle_resource_claim(request: Request, resource: str, resource_id: str) -> Response:
    """
    认领/取消认领资源。
    """
    # 验证资源类型
    if resource not in ['arxiv', 'github']:
        raise NotFound('资源类型不存在。')

    # 验证资源是否存在
    if resource == 'arxiv':
        if not ArxivEntry.objects.filter(arxiv_id=resource_id).exists():
            raise NotFound('ArXiv 论文不存在。')
    else:  # github
        if not GithubRepo.objects.filter(repo_id=resource_id).exists():
            raise NotFound('GitHub 仓库不存在。')

    # 尝试获取现有认领
    claim, created = ResourceClaim.objects.get_or_create(
        user=request.user,
        resource_type=resource,
        resource_id=resource_id
    )

    if not created:
        # 如果已存在认领，则取消认领
        claim.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # 返回新创建的认领
    serializer = ResourceClaimSerializer(claim)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
