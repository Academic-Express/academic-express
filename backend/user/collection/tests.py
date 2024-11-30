from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from pub.models import ArxivEntry, GithubRepo
from user.models import User

from .models import Collection


class CollectionTests(TestCase):
    def setUp(self):
        # 创建测试用户
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # 创建测试收藏夹
        self.collection = Collection.objects.create(
            user=self.user,
            name='Test Collection',
            description='Test Description',
            is_public=True
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
            link='https://arxiv.org/abs/2401.00001',
            pdf='https://arxiv.org/pdf/2401.00001'
        )

        # 创建测试 GitHub 仓库
        self.github_repo = GithubRepo.objects.create(
            repo_id=123456,
            name='test-repo',
            full_name='testuser/test-repo',
            description='Test Repository',
            html_url='https://github.com/testuser/test-repo',
            owner={
                'login': 'testuser',
                'id': 1,
                'type': 'User',
                'avatar_url': 'https://github.com/testuser.png'
            },
            created_at='2024-01-01T00:00:00Z',
            updated_at='2024-01-01T00:00:00Z',
            pushed_at='2024-01-01T00:00:00Z',
            language='Python',
            topics=['test']
        )

    def test_create_collection(self):
        """测试创建收藏夹"""
        url = reverse('collection-list')
        data = {
            'name': 'New Collection',
            'description': 'New Description',
            'is_public': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Collection.objects.count(), 2)
        self.assertEqual(Collection.objects.get(
            name='New Collection').description, 'New Description')

    def test_list_collections(self):
        """测试列出收藏夹"""
        url = reverse('collection-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Collection')

    def test_retrieve_collection(self):
        """测试获取单个收藏夹详情"""
        url = reverse('collection-detail', kwargs={'pk': self.collection.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Collection')
        self.assertEqual(response.data['items'], [])

    def test_update_collection(self):
        """测试更新收藏夹"""
        url = reverse('collection-detail', kwargs={'pk': self.collection.pk})
        data = {
            'name': 'Updated Collection',
            'description': 'Updated Description',
            'is_public': False
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.collection.refresh_from_db()
        self.assertEqual(self.collection.name, 'Updated Collection')
        self.assertEqual(self.collection.is_public, False)

    def test_delete_collection(self):
        """测试删除收藏夹"""
        url = reverse('collection-detail', kwargs={'pk': self.collection.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Collection.objects.count(), 0)

    def test_add_arxiv_to_collection(self):
        """测试添加 ArXiv 论文到收藏夹"""
        url = reverse('collection-add-item', kwargs={'pk': self.collection.pk})
        data = {
            'type': 'arxiv',
            'id': self.arxiv_entry.arxiv_id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 验证论文已被添加到收藏夹
        url = reverse('collection-detail', kwargs={'pk': self.collection.pk})
        response = self.client.get(url)
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(response.data['items'][0]['type'], 'arxiv')
        self.assertEqual(
            response.data['items'][0]['item']['arxiv_id'], self.arxiv_entry.arxiv_id)

    def test_add_github_to_collection(self):
        """测试添加 GitHub 仓库到收藏夹"""
        url = reverse('collection-add-item', kwargs={'pk': self.collection.pk})
        data = {
            'type': 'github',
            'id': self.github_repo.repo_id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 验证仓库已被添加到收藏夹
        url = reverse('collection-detail', kwargs={'pk': self.collection.pk})
        response = self.client.get(url)
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(response.data['items'][0]['type'], 'github')
        self.assertEqual(
            int(response.data['items'][0]['item']
                ['repo_id']), self.github_repo.repo_id
        )

    def test_remove_item_from_collection(self):
        """测试从收藏夹移除项目"""
        # 先添加一个项目
        self.collection.arxiv_entries.add(self.arxiv_entry)

        url = reverse('collection-remove-item',
                      kwargs={'pk': self.collection.pk})
        data = {
            'type': 'arxiv',
            'id': self.arxiv_entry.arxiv_id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 验证项目已被移除
        url = reverse('collection-detail', kwargs={'pk': self.collection.pk})
        response = self.client.get(url)
        self.assertEqual(len(response.data['items']), 0)

    def test_unauthorized_access(self):
        """测试未授权访问"""
        # 创建新用户的收藏夹
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        other_collection = Collection.objects.create(
            user=other_user,
            name='Other Collection',
            description='Other Description',
            is_public=False
        )

        # 尝试访问其他用户的私有收藏夹
        url = reverse('collection-detail', kwargs={'pk': other_collection.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_collection_with_empty_name(self):
        """测试创建空名称的收藏夹"""
        url = reverse('collection-list')
        data = {
            'name': '',
            'description': 'Description',
            'is_public': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_collection_with_long_name(self):
        """测试创建超长名称的收藏夹"""
        url = reverse('collection-list')
        data = {
            'name': 'a' * 101,  # 超过100字符限制
            'description': 'Description',
            'is_public': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_duplicate_item_to_collection(self):
        """测试重复添加同一项目到收藏夹"""
        # 第一次添加
        url = reverse('collection-add-item', kwargs={'pk': self.collection.pk})
        data = {
            'type': 'arxiv',
            'id': self.arxiv_entry.arxiv_id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 重复添加
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 验证只有一个项目被添加
        url = reverse('collection-detail', kwargs={'pk': self.collection.pk})
        response = self.client.get(url)
        self.assertEqual(len(response.data['items']), 1)

    def test_add_nonexistent_item(self):
        """测试添加不存在的项目"""
        url = reverse('collection-add-item', kwargs={'pk': self.collection.pk})
        data = {
            'type': 'arxiv',
            'id': 'nonexistent_id'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_nonexistent_item(self):
        """测试移除不存在的项目"""
        url = reverse('collection-remove-item',
                      kwargs={'pk': self.collection.pk})
        data = {
            'type': 'arxiv',
            'id': 'nonexistent_id'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_item_type(self):
        """测试无效的项目类型"""
        url = reverse('collection-add-item', kwargs={'pk': self.collection.pk})
        data = {
            'type': 'invalid_type',
            'id': '123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_public_collection_access(self):
        """测试公开收藏夹的访问权限"""
        # 创建另一个用户
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        other_client = APIClient()
        other_client.force_authenticate(user=other_user)

        # 尝试访问公开收藏夹
        url = reverse('collection-detail', kwargs={'pk': self.collection.pk})
        response = other_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_collection_items_ordering(self):
        """测试收藏项目的排序"""
        # 添加多个项目
        self.collection.arxiv_entries.add(self.arxiv_entry)
        self.collection.github_repos.add(self.github_repo)

        url = reverse('collection-detail', kwargs={'pk': self.collection.pk})
        response = self.client.get(url)

        # 验证按时间倒序排序
        items = response.data['items']
        self.assertEqual(len(items), 2)
        for i in range(len(items) - 1):
            self.assertGreaterEqual(
                items[i]['created_at'],
                items[i + 1]['created_at']
            )

    def test_collection_update_with_invalid_data(self):
        """测试使用无效数据更新收藏夹"""
        url = reverse('collection-detail', kwargs={'pk': self.collection.pk})
        data = {
            'name': '',  # 空名称
            'description': 'Updated Description',
            'is_public': False
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_collection_partial_update(self):
        """测试部分更新收藏夹"""
        url = reverse('collection-detail', kwargs={'pk': self.collection.pk})
        data = {
            'description': 'Only Update Description'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.collection.refresh_from_db()
        self.assertEqual(self.collection.description,
                         'Only Update Description')
        self.assertEqual(self.collection.name, 'Test Collection')  # 原名称保持不变

    def test_bulk_operations(self):
        """测试批量操作"""
        # 创建多个收藏夹
        collections = []
        for i in range(5):
            collections.append(Collection.objects.create(
                user=self.user,
                name=f'Collection {i}',
                description=f'Description {i}',
                is_public=True
            ))

        # 测试批量获取
        url = reverse('collection-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6)  # 5个新建的 + 1个setUp中的

        # 测试批量删除
        for collection in collections:
            url = reverse('collection-detail', kwargs={'pk': collection.pk})
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # 验证删除结果
        self.assertEqual(Collection.objects.count(), 1)  # 只剩下setUp中的收藏夹
