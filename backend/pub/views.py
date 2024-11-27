from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from utils.exceptions import ErrorSerializer

from .models import ArxivEntry, GithubRepo, Collection
from .serializers import ArxivEntrySerializer, GithubRepoSerializer, CollectionSerializer


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


@extend_schema(
    operation_id='list_or_create_collection',
    request=CollectionSerializer,
    responses={
        200: OpenApiResponse(CollectionSerializer(many=True), description='获取收藏列表成功'),
        201: OpenApiResponse(CollectionSerializer, description='创建收藏成功'),
        400: OpenApiResponse(ErrorSerializer, description='请求参数错误'),
    },
)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def list_or_create_collection(request: Request):
    """获取收藏列表或创建收藏"""
    if request.method == 'GET':
        collections = Collection.objects.filter(user=request.user)
        serializer = CollectionSerializer(collections, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(
    operation_id='delete_collection',
    responses={
        204: OpenApiResponse(None, description='删除收藏成功'),
        404: OpenApiResponse(ErrorSerializer, description='收藏不存在'),
    },
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_collection(request: Request, collection_id: int):
    """删除收藏"""
    try:
        collection = Collection.objects.get(pk=collection_id, user=request.user)
    except Collection.DoesNotExist:
        raise NotFound('收藏不存在')
    
    collection.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
