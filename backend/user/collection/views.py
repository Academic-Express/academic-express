from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from pub.models import ArxivEntry, GithubRepo

from .models import (Collection, CollectionArxivEntry, CollectionGithubRepo,
                     CollectionItem)
from .serializers import CollectionItemSerializer, CollectionSerializer


class CollectionViewSet(viewsets.ModelViewSet):
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Collection.objects.filter(
            Q(user=self.request.user) |  # 用户自己的收藏夹
            Q(is_public=True)  # 其他用户的公开收藏夹
        )

    def get_collection_items(self, collection):
        items = []
        # 获取 ArXiv 论文收藏
        arxiv_items = CollectionArxivEntry.objects.filter(
            collection=collection)
        for item in arxiv_items:
            items.append({
                'type': 'arxiv',
                'item': item.entry,
                'created_at': item.collection_time
            })

        # 获取 GitHub 仓库收藏
        github_items = CollectionGithubRepo.objects.filter(
            collection=collection)
        for item in github_items:
            items.append({
                'type': 'github',
                'item': item.repo,
                'created_at': item.collection_time
            })

        # 按收藏时间排序
        items.sort(key=lambda x: x['created_at'], reverse=True)
        return items

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        collection = self.get_object()
        item_type = request.data.get('type')
        item_id = request.data.get('id')

        if item_type == 'arxiv':
            entry = get_object_or_404(ArxivEntry, arxiv_id=item_id)
            CollectionArxivEntry.objects.get_or_create(
                collection=collection, entry=entry)
        elif item_type == 'github':
            repo = get_object_or_404(GithubRepo, repo_id=item_id)
            CollectionGithubRepo.objects.get_or_create(
                collection=collection, repo=repo)
        else:
            return Response({'error': 'Invalid item type'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def remove_item(self, request, pk=None):
        collection = self.get_object()
        item_type = request.data.get('type')
        item_id = request.data.get('id')

        if item_type == 'arxiv':
            CollectionArxivEntry.objects.filter(
                collection=collection,
                entry__arxiv_id=item_id
            ).delete()
        elif item_type == 'github':
            CollectionGithubRepo.objects.filter(
                collection=collection,
                repo__repo_id=item_id
            ).delete()
        else:
            return Response({'error': 'Invalid item type'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)

    def get_object(self):
        obj = super().get_object()
        # 如果是非公开收藏夹，确保只有所有者能访问
        if not obj.is_public and obj.user != self.request.user:
            raise Http404
        return obj

    def perform_create(self, serializer):
        """创建收藏夹时自动设置当前用户"""
        serializer.save(user=self.request.user)


class CollectionItemViewSet(viewsets.ModelViewSet):
    serializer_class = CollectionItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        collection_id = self.kwargs['collection_pk']
        return CollectionItem.objects.filter(
            collection_id=collection_id,
            collection__user=self.request.user
        )

    def perform_create(self, serializer):
        collection_id = self.kwargs['collection_pk']
        collection = Collection.objects.get(
            id=collection_id, user=self.request.user)
        serializer.save(collection=collection)
