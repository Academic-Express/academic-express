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
        if parent := serializer.validated_data.get('parent'):
            if parent.resource != resource:
                raise CustomValidationError({
                    'parent': ["回复的评论不属于当前资源"],
                })
            if parent.parent:
                raise CustomValidationError({
                    'parent': ["不支持多级回复"],
                })
        serializer.save(author=self.request.user, resource=resource)

    def perform_update(self, serializer):
        comment = self.get_object()
        if comment.author != self.request.user:
            self.permission_denied(
                self.request, message="无法修改其他用户的评论")

        if 'parent' in serializer.validated_data:
            raise CustomValidationError({
                'parent': ["无法修改评论的父评论"],
            })
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            self.permission_denied(
                self.request, message="无法删除其他用户的评论")
        instance.delete()

    @action(detail=True, methods=['post'])
    def vote(self, request, resource, pk=None):
        comment = self.get_object()
        serializer = VoteSerializer(data=request.data)

        if not serializer.is_valid():
            raise CustomValidationError(serializer.errors)

        value = serializer.validated_data['value']
        if value == Comment.VOTE_CANCEL:
            # 取消投票
            comment.votes.filter(user=request.user).delete()
        else:
            vote, created = Vote.objects.update_or_create(
                comment=comment,
                user=request.user,
                defaults={'value': value}
            )

        # Return updated comment data
        comment_serializer = CommentSerializer(comment, context={'request': request})
        return Response(comment_serializer.data, status=status.HTTP_200_OK)

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
                {"detail": "无法修改其他用户的评论"},
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
                {"detail": "无法删除其他用户的评论"},
                status=status.HTTP_403_FORBIDDEN
            )

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
