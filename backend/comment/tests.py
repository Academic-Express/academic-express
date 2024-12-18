from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from comment.models import Comment, Vote
from user.models import User


class CommentTests(APITestCase):
    client: APIClient

    def setUp(self):
        # 创建测试用户
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='testpass123',
            email='test1@example.com'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='testpass123',
            email='test2@example.com'
        )

        # 设置测试客户端
        self.client = APIClient()

        # 测试资源标识符
        self.resource = 'arxiv/2401.00001'

        # 创建一些初始评论
        self.comment1 = Comment.objects.create(
            resource=self.resource,
            content='Test comment 1',
            author=self.user1
        )
        self.comment2 = Comment.objects.create(
            resource=self.resource,
            content='Test comment 2',
            author=self.user2,
            parent=self.comment1
        )

    def test_get_comments(self):
        """测试获取评论列表"""
        url = reverse('comment-list', kwargs={'resource': self.resource})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # 只返回顶层评论
        self.assertEqual(len(response.data[0]['replies']), 1)  # 包含一个回复

    def test_create_comment(self):
        """测试创建新评论"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('comment-list', kwargs={'resource': self.resource})

        # 创建顶层评论
        data = {'content': 'New top-level comment'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 创建回复
        data = {
            'content': 'New reply',
            'parent': self.comment1.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['parent'], self.comment1.id)

        # 创建回复时指定无效的父评论
        data = {
            'content': 'Invalid reply',
            'parent': 0
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 创建回复时指定属于其他资源的父评论
        data = {
            'content': 'Invalid reply',
            'parent': self.comment2.id
        }
        url = reverse('comment-list', kwargs={'resource': 'arxiv/2401.00002'})
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_comment(self):
        """测试更新评论"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('comment-detail', kwargs={
            'resource': self.resource,
            'pk': self.comment1.id
        })

        # 更新自己的评论
        data = {'content': 'Updated content'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Updated content')

        # 尝试更新他人的评论
        self.client.force_authenticate(user=self.user2)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_comment(self):
        """测试删除评论"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('comment-detail', kwargs={
            'resource': self.resource,
            'pk': self.comment1.id
        })

        # 尝试删除他人的评论
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # 删除自己的评论
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_vote_comment(self):
        """测试评论投票"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('comment-vote', kwargs={
            'resource': self.resource,
            'pk': self.comment2.id
        })

        # 投赞成票
        response = self.client.post(url, {'value': Comment.VOTE_UP})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 检查投票是否被记录
        vote = Vote.objects.get(comment=self.comment2, user=self.user1)
        self.assertEqual(vote.value, Comment.VOTE_UP)

        # 改变投票
        response = self.client.post(url, {'value': Comment.VOTE_DOWN})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 检查投票是否被更新
        vote.refresh_from_db()
        self.assertEqual(vote.value, Comment.VOTE_DOWN)

        # 取消投票
        response = self.client.post(url, {'value': Comment.VOTE_CANCEL})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 检查投票是否被删除
        self.assertFalse(Vote.objects.filter(comment=self.comment2, user=self.user1).exists())

    def test_unauthorized_access(self):
        """测试未认证访问限制"""
        url = reverse('comment-list', kwargs={'resource': self.resource})

        # 获取评论列表应该允许
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 其他操作应该被拒绝
        data = {'content': 'Unauthorized comment'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_vote_value(self):
        """测试无效的投票值"""
        self.client.force_authenticate(user=self.user1)
        url = reverse('comment-vote', kwargs={
            'resource': self.resource,
            'pk': self.comment1.id
        })

        # 尝试使用无效的投票值
        response = self.client.post(url, {'value': 2})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_vote_count(self):
        """测试投票计数"""
        self.client.force_authenticate(user=self.user1)

        # 创建一个新的评论用于测试
        test_comment = Comment.objects.create(
            resource=self.resource,
            content='Test comment for voting',
            author=self.user1
        )

        # 获取评论详情检查初始投票数
        url = reverse('comment-detail', kwargs={
            'resource': self.resource,
            'pk': test_comment.id
        })
        response = self.client.get(url)
        self.assertEqual(response.data['vote_count'], 0)

        # 用户1投赞成票
        vote_url = reverse('comment-vote', kwargs={
            'resource': self.resource,
            'pk': test_comment.id
        })
        response = self.client.post(vote_url, {'value': Comment.VOTE_UP})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 检查投票后的计数
        response = self.client.get(url)
        self.assertEqual(response.data['vote_count'], 1)

        # 用户2投反对票
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(vote_url, {'value': Comment.VOTE_DOWN})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 再次获取评论详情检查最终投票数
        response = self.client.get(url)
        self.assertEqual(response.data['vote_count'], 0)  # 1 + (-1) = 0
