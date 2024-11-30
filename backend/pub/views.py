from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from utils.exceptions import ErrorSerializer

from .models import ArxivEntry, GithubRepo
from .serializers import ArxivEntrySerializer, GithubRepoSerializer


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
def get_github_repo(request: Request, owner: str, repo: str):
    """
    获取 Github 仓库。
    """
    try:
        repo = GithubRepo.objects.get(full_name=f'{owner}/{repo}')
    except GithubRepo.DoesNotExist:
        raise NotFound('Github 仓库不存在。')

    serializer = GithubRepoSerializer(repo)
    return Response(serializer.data, status=status.HTTP_200_OK)
