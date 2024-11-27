from datetime import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model

from .models import ArxivEntry, Collection, CollectionGroup

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


class CollectionTests(APITestCase):
    def setUp(self):
        # 创建测试用户
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123'
        )
        # 创建测试论文
        self.arxiv_entry = ArxivEntry.objects.create(
            arxiv_id='test123',
            title='Test Paper',
            summary='Test Summary',
            authors=[{'name': 'Test Author'}],
            published='2024-01-01T00:00:00Z',
            updated='2024-01-01T00:00:00Z',
            primary_category='cs.AI',
            categories=['cs.AI'],
            link='http://example.com',
            pdf='http://example.com/pdf'
        )

        # 认证客户端
        self.client.force_authenticate(user=self.user)

    def test_create_collection(self):
        """测试创建收藏"""
        url = reverse('pub:list_or_create_collection')
        data = {
            'arxiv_entry': self.arxiv_entry.arxiv_id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Collection.objects.count(), 1)
        self.assertEqual(Collection.objects.first().user, self.user)

    def test_list_collections(self):
        """测试获取收藏列表"""
        Collection.objects.create(
            user=self.user,
            arxiv_entry=self.arxiv_entry
        )

        url = reverse('pub:list_or_create_collection')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_delete_collection(self):
        """测试删除收藏"""
        collection = Collection.objects.create(
            user=self.user,
            arxiv_entry=self.arxiv_entry
        )

        url = reverse('pub:delete_collection', kwargs={
                      'collection_id': collection.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Collection.objects.count(), 0)

    def test_delete_nonexistent_collection(self):
        """测试删除不存在的收藏"""
        url = reverse('pub:delete_collection', kwargs={'collection_id': 999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_access(self):
        """测试未认证访问"""
        self.client.force_authenticate(user=None)
        url = reverse('pub:list_or_create_collection')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CollectionGroupTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = get_user_model().objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.collection = Collection.objects.create(
            user=self.user,
            arxiv_entry=ArxivEntry.objects.create(
                arxiv_id='test123',
                title='Test Paper',
                summary='Test Summary',
                authors=[{'name': 'Test Author'}],
                published='2024-01-01T00:00:00Z',
                updated='2024-01-01T00:00:00Z',
                primary_category='cs.AI',
                categories=['cs.AI'],
                link='http://example.com',
                pdf='http://example.com/pdf'
            )
        )

    def test_create_collection_group(self):
        """测试创建收藏分组"""
        url = reverse('pub:list_or_create_collection_group')
        data = {'name': 'My Group', 'collections': [self.collection.id]}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CollectionGroup.objects.count(), 1)
        self.assertEqual(CollectionGroup.objects.first().name, 'My Group')

    def test_create_group_with_empty_name(self):
        """测试创建空名称的收藏分组"""
        url = reverse('pub:list_or_create_collection_group')
        data = {'name': '', 'collections': [self.collection.id]}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_nonexistent_collection_to_group(self):
        """测试添加不存在的收藏到分组"""
        url = reverse('pub:list_or_create_collection_group')
        data = {'name': 'My Group', 'collections': [999]}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_collection_groups(self):
        """测试获取收藏分组列表"""
        CollectionGroup.objects.create(user=self.user, name='My Group')
        url = reverse('pub:list_or_create_collection_group')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_collection_group(self):
        """测试获取收藏分组内容"""
        group = CollectionGroup.objects.create(user=self.user, name='My Group')
        url = reverse('pub:retrieve_update_delete_collection_group',
                      kwargs={'group_id': group.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'My Group')

    def test_update_collection_group(self):
        """测试更新收藏分组信息"""
        group = CollectionGroup.objects.create(user=self.user, name='My Group')
        url = reverse('pub:retrieve_update_delete_collection_group',
                      kwargs={'group_id': group.id})
        data = {'name': 'Updated Group'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        group.refresh_from_db()
        self.assertEqual(group.name, 'Updated Group')

    def test_update_group_with_invalid_data(self):
        """测试更新分组为无效数据"""
        group = CollectionGroup.objects.create(user=self.user, name='My Group')
        url = reverse('pub:retrieve_update_delete_collection_group',
                      kwargs={'group_id': group.id})
        data = {'name': ''}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_collection_group(self):
        """测试删除收藏分组"""
        group = CollectionGroup.objects.create(user=self.user, name='My Group')
        url = reverse('pub:retrieve_update_delete_collection_group',
                      kwargs={'group_id': group.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CollectionGroup.objects.count(), 0)

    def test_delete_other_users_group(self):
        """测试删除其他用户的分组"""
        group = CollectionGroup.objects.create(
            user=self.other_user, name='Other Group')
        url = reverse('pub:retrieve_update_delete_collection_group',
                      kwargs={'group_id': group.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_other_users_group(self):
        """测试获取其他用户的分组"""
        group = CollectionGroup.objects.create(
            user=self.other_user, name='Other Group')
        url = reverse('pub:retrieve_update_delete_collection_group',
                      kwargs={'group_id': group.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
