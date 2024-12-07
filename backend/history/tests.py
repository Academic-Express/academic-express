from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from pub.models import ArxivEntry, GithubRepo

from .models import History

User = get_user_model()


class HistoryAPITest(APITestCase):
    def setUp(self):
        # 创建测试用户
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

        # 创建测试 ArXiv 论文
        self.arxiv_paper = ArxivEntry.objects.create(
            arxiv_id='2312.12345',
            title='Test Paper',
            summary='Test summary',
            authors=[{'name': 'John Doe', 'affiliation': 'Test University'}],
            published='2023-12-07T12:00:00Z',
            updated='2023-12-07T12:00:00Z',
            primary_category='cs.AI',
            categories=['cs.AI', 'cs.LG'],
            link='https://arxiv.org/abs/2312.12345',
            pdf='https://arxiv.org/pdf/2312.12345.pdf'
        )

        # 创建测试 GitHub 仓库
        self.github_repo = GithubRepo.objects.create(
            repo_id='12345',
            name='test-repo',
            full_name='testuser/test-repo',
            description='Test repository',
            html_url='https://github.com/testuser/test-repo',
            owner={'login': 'testuser'},
            created_at='2023-12-07T12:00:00Z',
            updated_at='2023-12-07T12:00:00Z',
            pushed_at='2023-12-07T12:00:00Z',
            topics=[],
        )

    def test_arxiv_paper_view_creates_history(self):
        """测试访问 ArXiv 论文时创建历史记录"""
        url = reverse('pub:get_arxiv_entry', kwargs={
                      'arxiv_id': self.arxiv_paper.arxiv_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 验证历史记录是否创建
        history = History.objects.filter(
            user=self.user,
            arxiv_entry=self.arxiv_paper
        ).first()

        self.assertIsNotNone(history)
        self.assertEqual(history.content_type, 'arxiv')
        self.assertEqual(history.arxiv_entry.title, self.arxiv_paper.title)

    def test_github_repo_view_creates_history(self):
        """测试访问 GitHub 仓库时创建历史记录"""
        owner = self.github_repo.full_name.split('/')[0]
        repo = self.github_repo.name
        url = reverse('pub:get_github_repo', kwargs={
                      'owner': owner, 'repo': repo})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 验证历史记录是否创建
        history = History.objects.filter(
            user=self.user,
            github_repo=self.github_repo
        ).first()

        self.assertIsNotNone(history)
        self.assertEqual(history.content_type, 'github')
        self.assertEqual(history.github_repo.full_name, self.github_repo.full_name)

    def test_repeated_views_update_history(self):
        """测试重复访问同一资源时更新历史记录"""
        url = reverse('pub:get_arxiv_entry', kwargs={
                      'arxiv_id': self.arxiv_paper.arxiv_id})

        # 第一次访问
        self.client.get(url)
        first_view = History.objects.get(
            user=self.user,
            arxiv_entry=self.arxiv_paper
        )
        first_viewed_at = first_view.viewed_at

        # 等待一小段时间后再次访问
        import time
        time.sleep(1)

        # 第二次访问
        self.client.get(url)
        second_view = History.objects.get(
            user=self.user,
            arxiv_entry=self.arxiv_paper
        )

        # 验证是同一条记录但访问时间已更新
        self.assertEqual(first_view.id, second_view.id)
        self.assertGreater(second_view.viewed_at, first_viewed_at)

    def test_unauthenticated_user_no_history(self):
        """测试未登录用户访问不会创建历史记录"""
        self.client.force_authenticate(user=None)
        url = reverse('pub:get_arxiv_entry', kwargs={
                      'arxiv_id': self.arxiv_paper.arxiv_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(History.objects.count(), 0)
