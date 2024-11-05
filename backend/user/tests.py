from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import User

# Create your tests here.


class UserTests(APITestCase):
    client: APIClient

    def setUp(self):
        self.test_user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'nickname': 'testnickname',
            'email': 'testuser@example.com',
            'phone': '1234567890',
            'url': 'http://example.com',
        }
        self.test_user = User.objects.create_user(**self.test_user_data)

    def test_register(self):
        """
        测试注册用户。
        """
        url = reverse('user:register')
        data = {
            'username': 'newuser',
            'password': 'newpassword',
            'nickname': 'newnickname',
            'email': 'newuser@example.com',
            'phone': '0987654321',
            'url': 'http://newexample.com',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

        user = User.objects.get(username=data['username'])
        self.assertEqual(user.nickname, data['nickname'])
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.phone, data['phone'])
        self.assertEqual(user.url, data['url'])

    def test_get_current_user(self):
        """
        测试获取当前用户。
        """
        url = reverse('user:get_current_user')

        # 未登录时，返回 401。
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['code'], 'not_authenticated')

        # 登录后，返回当前用户信息。
        self.client.force_authenticate(user=self.test_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.test_user_data['username'])
        self.assertEqual(response.data['nickname'], self.test_user_data['nickname'])
        self.assertEqual(response.data['email'], self.test_user_data['email'])
        self.assertEqual(response.data['phone'], self.test_user_data['phone'])
        self.assertEqual(response.data['url'], self.test_user_data['url'])

    def test_get_user_by_id(self):
        """
        测试通过 ID 获取用户。
        """
        # 存在的用户，返回用户信息。
        url = reverse('user:get_user_by_id', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.test_user_data['username'])
        self.assertEqual(response.data['nickname'], self.test_user_data['nickname'])
        self.assertEqual(response.data['email'], self.test_user_data['email'])
        self.assertEqual(response.data['phone'], self.test_user_data['phone'])
        self.assertEqual(response.data['url'], self.test_user_data['url'])

        # 不存在的用户，返回 404。
        url = reverse('user:get_user_by_id', args=[233])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['code'], 'user_does_not_exist')

    def test_change_password(self):
        """
        测试修改密码。
        """
        url = reverse('user:change_password')

        # 未登录时，返回 401。
        data = {
            'old_password': 'oldpassword',
            'new_password': 'newpassword',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['code'], 'not_authenticated')

        # 旧密码错误时，返回 400。
        self.client.force_authenticate(user=self.test_user)
        data = {
            'old_password': 'wrongpassword',
            'new_password': 'newpassword',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['code'], 'password_not_match')

        # 旧密码正确时，修改成功。
        data = {
            'old_password': self.test_user_data['password'],
            'new_password': 'newpassword',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        user = User.objects.get(username=self.test_user_data['username'])
        self.assertTrue(user.check_password(data['new_password']))
