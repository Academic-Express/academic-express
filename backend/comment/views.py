from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from comment.models import Comment, Vote
from comment.serializers import CommentSerializer, VoteSerializer
from utils.exceptions import CustomValidationError


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        resource = self.kwargs.get('resource')
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy', 'vote']:
            # 对于单个评论的操作，返回所有评论
            return Comment.objects.filter(resource=resource)
        # 对于列表操作，只返回顶层评论
        return Comment.objects.filter(resource=resource, parent=None)

    def perform_create(self, serializer):
        resource = self.kwargs.get('resource')
        parent = serializer.validated_data.get('parent')
        if parent and parent.resource != resource:
            raise CustomValidationError({
                'parent': ["回复的评论不属于当前资源"],
            })
        serializer.save(author=self.request.user, resource=resource)

    def perform_update(self, serializer):
        comment = self.get_object()
        if comment.author != self.request.user:
            self.permission_denied(
                self.request, message="Cannot edit another user's comment")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            self.permission_denied(
                self.request, message="Cannot delete another user's comment")
        instance.delete()

    @action(detail=True, methods=['post'])
    def vote(self, request, resource, pk=None):
        comment = self.get_object()
        serializer = VoteSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        value = serializer.validated_data['value']

        try:
            vote, created = Vote.objects.update_or_create(
                comment=comment,
                user=request.user,
                defaults={'value': value}
            )
            # Return updated comment data
            comment_serializer = CommentSerializer(
                comment, context={'request': request})
            return Response(comment_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # 检查权限
        if instance.author != request.user:
            return Response(
                {"detail": "Cannot edit another user's comment"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # 检查权限
        if instance.author != request.user:
            return Response(
                {"detail": "Cannot delete another user's comment"},
                status=status.HTTP_403_FORBIDDEN
            )

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
