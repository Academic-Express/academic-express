from datetime import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from user.models import User

from .models import ArxivEntry, GithubRepo, ResourceClaim

# Create your tests here.


class PubTests(APITestCase):
    client: APIClient

    def setUp(self) -> None:
        self.test_arxiv_entry_data = {
            'arxiv_id': '1706.03762v7',
            'authors': [{'name': 'Ashish Vaswani'},
                        {'name': 'Noam Shazeer'},
                        {'name': 'Niki Parmar'},
                        {'name': 'Jakob Uszkoreit'},
                        {'name': 'Llion Jones'},
                        {'name': 'Aidan N. Gomez'},
                        {'name': 'Lukasz Kaiser'},
                        {'name': 'Illia Polosukhin'}],
            'categories': ['cs.CL', 'cs.LG'],
            'comment': '15 pages, 5 figures',
            'link': 'http://arxiv.org/abs/1706.03762v7',
            'pdf': 'http://arxiv.org/pdf/1706.03762v7',
            'primary_category': 'cs.CL',
            'published': '2017-06-12T17:57:34Z',
            'summary': 'The dominant sequence transduction models are based on complex '
            'recurrent or convolutional neural networks in an encoder-decoder '
            'configuration. The best performing models also connect the '
            'encoder and decoder through an attention mechanism. We propose a '
            'new simple network architecture, the Transformer, based solely on '
            'attention mechanisms, dispensing with recurrence and convolutions '
            'entirely. Experiments on two machine translation tasks show these '
            'models to be superior in quality while being more parallelizable '
            'and requiring significantly less time to train. Our model '
            'achieves 28.4 BLEU on the WMT 2014 English-to-German translation '
            'task, improving over the existing best results, including '
            'ensembles by over 2 BLEU. On the WMT 2014 English-to-French '
            'translation task, our model establishes a new single-model '
            'state-of-the-art BLEU score of 41.8 after training for 3.5 days '
            'on eight GPUs, a small fraction of the training costs of the best '
            'models from the literature. We show that the Transformer '
            'generalizes well to other tasks by applying it successfully to '
            'English constituency parsing both with large and limited training '
            'data.',
            'title': 'Attention Is All You Need',
            'updated': '2023-08-02T00:41:18Z'
        }
        self.test_arxiv_entry = ArxivEntry.objects.create(
            **self.test_arxiv_entry_data)

    def test_get_arxiv_entry(self):
        url = reverse('pub:get_arxiv_entry',
                      kwargs={'arxiv_id': self.test_arxiv_entry_data['arxiv_id']})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for k, v in self.test_arxiv_entry_data.items():
            if k in ('published', 'updated'):
                expected = datetime.fromisoformat(v)
                actual = datetime.fromisoformat(response.data[k])
                self.assertEqual(expected, actual)
            else:
                self.assertEqual(response.data[k], v)


class ResourceClaimTests(APITestCase):
    client: APIClient

    def setUp(self):
        # 创建测试用户
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            phone='1234567890',
            nickname='Test User'
        )
        self.another_user = User.objects.create_user(
            username='anotheruser',
            password='testpass123',
            email='another@example.com',
            phone='1234567891',
            nickname='Another User'
        )

        # 创建测试 ArXiv 论文
        self.arxiv_entry = ArxivEntry.objects.create(
            arxiv_id='2401.00001',
            title='Test Paper',
            summary='Test Summary',
            authors=[{'name': 'Test Author'}],
            published='2024-01-01T00:00:00Z',
            updated='2024-01-01T00:00:00Z',
            primary_category='cs.AI',
            categories=['cs.AI'],
            link='http://arxiv.org/abs/2401.00001',
            pdf='http://arxiv.org/pdf/2401.00001'
        )

        # 创建测试 GitHub 仓库
        self.github_repo = GithubRepo.objects.create(
            repo_id='12345',
            name='test-repo',
            full_name='testuser/test-repo',
            description='Test Repository',
            html_url='https://github.com/testuser/test-repo',
            owner={'login': 'testuser'},
            created_at='2024-01-01T00:00:00Z',
            updated_at='2024-01-01T00:00:00Z',
            pushed_at='2024-01-01T00:00:00Z',
            topics=['test']
        )

    def test_get_resource_claims_arxiv(self):
        """测试获取 ArXiv 论文的认领列表"""
        ResourceClaim.objects.create(
            user=self.user,
            resource_type='arxiv',
            resource_id=self.arxiv_entry.arxiv_id
        )

        url = reverse('pub:resource_claim', kwargs={
            'resource': 'arxiv',
            'resource_id': self.arxiv_entry.arxiv_id
        })
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user'], self.user.id)
        self.assertEqual(response.data[0]['resource_type'], 'arxiv')
        self.assertEqual(
            response.data[0]['resource_id'], self.arxiv_entry.arxiv_id)

    def test_get_resource_claims_github(self):
        """测试获取 GitHub 仓库的认领列表"""
        # 创建一些测试认领数据
        ResourceClaim.objects.create(
            user=self.user,
            resource_type='github',
            resource_id=self.github_repo.repo_id
        )

        url = reverse('pub:resource_claim', kwargs={
            'resource': 'github',
            'resource_id': self.github_repo.repo_id
        })
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user'], self.user.id)
        self.assertEqual(response.data[0]['resource_type'], 'github')
        self.assertEqual(
            response.data[0]['resource_id'], self.github_repo.repo_id)

    def test_toggle_resource_claim(self):
        """测试认领/取消认领资源"""
        self.client.force_authenticate(user=self.user)

        url = reverse('pub:resource_claim', kwargs={
            'resource': 'arxiv',
            'resource_id': self.arxiv_entry.arxiv_id
        })

        # 测试缺少 claim 参数
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 测试认领
        response = self.client.post(f"{url}?claim=true")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ResourceClaim.objects.filter(
            user=self.user,
            resource_type='arxiv',
            resource_id=self.arxiv_entry.arxiv_id
        ).exists())

        # 测试重复认领
        response = self.client.post(f"{url}?claim=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(ResourceClaim.objects.filter(
            user=self.user,
            resource_type='arxiv',
            resource_id=self.arxiv_entry.arxiv_id
        ).exists())

        # 测试取消认领
        response = self.client.post(f"{url}?claim=false")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ResourceClaim.objects.filter(
            user=self.user,
            resource_type='arxiv',
            resource_id=self.arxiv_entry.arxiv_id
        ).exists())

        # 测试重复取消认领
        response = self.client.post(f"{url}?claim=false")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ResourceClaim.objects.filter(
            user=self.user,
            resource_type='arxiv',
            resource_id=self.arxiv_entry.arxiv_id
        ).exists())

    def test_get_user_claims(self):
        """测试获取用户的全部认领"""
        # 创建一些测试认领数据
        ResourceClaim.objects.create(
            user=self.user,
            resource_type='arxiv',
            resource_id=self.arxiv_entry.arxiv_id
        )
        ResourceClaim.objects.create(
            user=self.user,
            resource_type='github',
            resource_id=self.github_repo.repo_id
        )

        url = reverse('user:get_user_claims', kwargs={'pk': self.user.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # 验证返回的数据包含所有认领
        resource_types = [claim['resource_type'] for claim in response.data]
        self.assertIn('arxiv', resource_types)
        self.assertIn('github', resource_types)

    def test_unauthorized_claim(self):
        """测试未认证用户无法认领资源"""
        url = reverse('pub:resource_claim', kwargs={
            'resource': 'arxiv',
            'resource_id': self.arxiv_entry.arxiv_id
        })
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_resource_type(self):
        """测试无效的资源类型"""
        url = reverse('pub:resource_claim', kwargs={
            'resource': 'invalid',
            'resource_id': '123'
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_nonexistent_resource(self):
        """测试不存在的资源"""
        url = reverse('pub:resource_claim', kwargs={
            'resource': 'arxiv',
            'resource_id': 'nonexistent'
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
