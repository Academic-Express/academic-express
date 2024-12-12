from django.core.exceptions import PermissionDenied
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import History
from .serializers import HistorySerializer


class HistoryViewSet(viewsets.ModelViewSet):
    serializer_class = HistorySerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        return History.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        content_type = request.data.get('content_type')

        # 验证content_type
        if content_type not in ['arxiv', 'github']:
            return Response(
                {'error': 'Invalid content type'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 准备数据
        data = request.data.copy()
        data['user'] = request.user.id

        # 创建或更新历史记录
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied()
        return obj
