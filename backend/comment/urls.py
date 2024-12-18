from django.urls import path
from comment.views import CommentViewSet

comment_vote = CommentViewSet.as_view({
    'post': 'vote'
})

comment_detail = CommentViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy'
})

comment_list = CommentViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

urlpatterns = [
    path('<path:resource>/<int:pk>/vote/', comment_vote, name='comment-vote'),
    path('<path:resource>/<int:pk>/', comment_detail, name='comment-detail'),
    path('<path:resource>/', comment_list, name='comment-list'),
]
