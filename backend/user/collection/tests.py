from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from pub.models import ArxivEntry, GithubRepo
from user.models import User

from .models import Collection, CollectionGroup


class CollectionTests(TestCase):
    def setUp(self):
        # 创建测试用户
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

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

    def test_add_collection(self):
        """测试添加收藏"""
        url = reverse('collection:collection-list')

        # 测试添加 ArXiv 论文
        data = {
            'type': 'arxiv',
            'id': self.arxiv_entry.arxiv_id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 测试添加 GitHub 仓库
        data = {
            'type': 'github',
            'id': self.github_repo.repo_id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_collections(self):
        """测试列出收藏"""
        # 先添加一些收藏
        Collection.objects.create(
            user=self.user,
            item_type='arxiv',
            item_id=self.arxiv_entry.arxiv_id
        )
        Collection.objects.create(
            user=self.user,
            item_type='github',
            item_id=str(self.github_repo.repo_id)
        )

        url = reverse('collection:collection-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_delete_collection(self):
        """测试删除收藏"""
        collection = Collection.objects.create(
            user=self.user,
            item_type='arxiv',
            item_id=self.arxiv_entry.arxiv_id
        )

        url = reverse('collection:collection-detail', kwargs={'pk': collection.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Collection.objects.count(), 0)

    def test_update_collection(self):
        """测试更新收藏项"""
        collection = Collection.objects.create(
            user=self.user,
            item_type='arxiv',
            item_id=self.arxiv_entry.arxiv_id
        )

        url = reverse('collection:collection-detail', kwargs={'pk': collection.id})
        data = {
            'item_type': 'github',
            'item_id': str(self.github_repo.repo_id)
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        collection.refresh_from_db()
        self.assertEqual(collection.item_type, 'github')
        self.assertEqual(collection.item_id, str(self.github_repo.repo_id))

    def test_retrieve_collection(self):
        """测试获取单个收藏项"""
        collection = Collection.objects.create(
            user=self.user,
            item_type='arxiv',
            item_id=self.arxiv_entry.arxiv_id
        )

        url = reverse('collection:collection-detail', kwargs={'pk': collection.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['item_type'], 'arxiv')
        self.assertEqual(response.data['item_id'], self.arxiv_entry.arxiv_id)


class CollectionGroupTests(TestCase):
    def setUp(self):
        # 创建测试用户
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # 创建测试收藏
        self.collection = Collection.objects.create(
            user=self.user,
            item_type='arxiv',
            item_id='2401.00001'
        )

    def test_create_group(self):
        """测试创建收藏分组"""
        url = reverse('collection:collectiongroup-list')
        data = {
            'name': 'Test Group',
            'description': 'Test Description',
            'is_public': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CollectionGroup.objects.count(), 1)

    def test_list_groups(self):
        """测试列出收藏分组"""
        CollectionGroup.objects.create(
            user=self.user,
            name='Test Group 1',
            description='Test Description 1'
        )
        CollectionGroup.objects.create(
            user=self.user,
            name='Test Group 2',
            description='Test Description 2'
        )

        url = reverse('collection:collectiongroup-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_manage_group_items(self):
        """测试管理分组内的收藏项"""
        group = CollectionGroup.objects.create(
            user=self.user,
            name='Test Group',
            description='Test Description'
        )

        url = reverse('collection:collectiongroup-manage-items', kwargs={'pk': group.id})

        # 测试添加收藏到分组
        data = {
            'action': 'add',
            'collection_ids': [self.collection.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 验证收藏已被添加到分组
        group = CollectionGroup.objects.get(id=group.id)
        self.assertEqual(group.collections.count(), 1)

        # 测试从分组移除收藏
        data = {
            'action': 'remove',
            'collection_ids': [self.collection.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 验证收藏已从分组移除
        group = CollectionGroup.objects.get(id=group.id)
        self.assertEqual(group.collections.count(), 0)

    def test_update_group(self):
        """测试更新分组信息"""
        group = CollectionGroup.objects.create(
            user=self.user,
            name='Test Group',
            description='Test Description'
        )

        url = reverse('collection:collectiongroup-detail', kwargs={'pk': group.id})
        data = {
            'name': 'Updated Group',
            'description': 'Updated Description'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        group.refresh_from_db()
        self.assertEqual(group.name, 'Updated Group')
        self.assertEqual(group.description, 'Updated Description')

    def test_retrieve_group(self):
        """测试获取单个收藏分组"""
        group = CollectionGroup.objects.create(
            user=self.user,
            name='Test Group',
            description='Test Description'
        )

        url = reverse('collection:collectiongroup-detail', kwargs={'pk': group.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Group')

    def test_toggle_group_visibility(self):
        """测试切换分组的公开/私有状态"""
        group = CollectionGroup.objects.create(
            user=self.user,
            name='Test Group',
            description='Test Description',
            is_public=True
        )

        url = reverse('collection:collectiongroup-detail', kwargs={'pk': group.id})
        data = {'is_public': False}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        group.refresh_from_db()
        self.assertFalse(group.is_public)

        # 再次切换回公开
        data = {'is_public': True}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        group.refresh_from_db()
        self.assertTrue(group.is_public)

    def test_delete_group(self):
        """测试删除分组"""
        group = CollectionGroup.objects.create(
            user=self.user,
            name='Test Group',
            description='Test Description'
        )

        url = reverse('collection:collectiongroup-detail', kwargs={'pk': group.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CollectionGroup.objects.count(), 0)
