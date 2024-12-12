from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from utils.exceptions import ErrorSerializer

from .models import Collection, CollectionGroup, GroupCollection
from .serializers import (CollectionGroupManageItemsSerializer,
                          CollectionGroupSerializer, CollectionSerializer)


class CollectionViewSet(viewsets.ModelViewSet):
    """收藏项的视图集"""
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Collection.objects.filter(user=self.request.user)

    def perform_create(self, serializer: CollectionSerializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CollectionGroupViewSet(viewsets.ModelViewSet):
    """收藏分组的视图集"""
    serializer_class = CollectionGroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CollectionGroup.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        operation_id='collection_group_manage_items',
        request=CollectionGroupManageItemsSerializer,
        responses={
            200: OpenApiResponse(CollectionGroupSerializer, description='管理收藏分组成功'),
            400: OpenApiResponse(ErrorSerializer, description='请求数据有误'),
        },
    )
    @action(detail=True, methods=['post'])
    def manage_items(self, request, pk=None):
        """
        添加或移除收藏分组的收藏项。

        - 添加收藏项：action='add'，collection_ids 为要添加的收藏项 ID 列表。
        - 移除收藏项：action='remove'，collection_ids 为要移除的收藏项 ID 列表。
        """
        group = self.get_object()

        request_serializer = CollectionGroupManageItemsSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        action = request_serializer.validated_data['action']
        collection_ids = request_serializer.validated_data['collection_ids']

        collections = Collection.objects.filter(
            id__in=collection_ids,
            user=request.user
        )

        if action == 'add':
            for collection in collections:
                GroupCollection.objects.get_or_create(
                    group=group,
                    collection=collection
                )
        else:  # action == 'remove'
            GroupCollection.objects.filter(
                group=group,
                collection_id__in=collection_ids
            ).delete()

        serializer = self.get_serializer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)
