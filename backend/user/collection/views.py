from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Collection, CollectionGroup, GroupCollection
from .serializers import CollectionGroupSerializer, CollectionSerializer


class CollectionViewSet(viewsets.ModelViewSet):
    """收藏项的视图集"""
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Collection.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = {
            'item_type': request.data.get('type'),
            'item_id': request.data.get('id'),
        }
        serializer = self.get_serializer(data=data)
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

    @action(detail=True, methods=['post'])
    def manage_items(self, request, pk=None):
        group = self.get_object()
        action = request.data.get('action')
        collection_ids = request.data.get('collection_ids', [])

        if not isinstance(collection_ids, list):
            return Response(
                {'error': 'collection_ids must be a list'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if action not in ['add', 'remove']:
            return Response(
                {'error': 'Invalid action. Must be either "add" or "remove"'},
                status=status.HTTP_400_BAD_REQUEST
            )

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
