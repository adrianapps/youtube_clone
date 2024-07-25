import os

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from channel.models import User
from .factories import UserFactory, ChannelFactory


class RegisterTest(APITestCase):
    def test_post(self):
        url = reverse('api_channel:register')
        data = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'testing321'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')


class UserListTest(APITestCase):
    def setUp(self):
        self.url = reverse('api_channel:user-list')
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserDetailTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.url = reverse('api_channel:user-detail', kwargs={'user_id': self.user.id})
        self.client.force_authenticate(user=self.user)

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ChannelListTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.channel = ChannelFactory()
        self.url = reverse('api_channel:channel-list')
        self.client.force_authenticate(user=self.user)
        self.data = {
            'name': "Test Channel",
            'user': self.user.id,
            'description': "Some description"
        }

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ChannelDetailTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.subscribers = UserFactory.create_batch(3)
        self.channel = ChannelFactory(user=self.user, subscribers=self.subscribers)
        self.url = reverse('api_channel:channel-detail', kwargs={'channel_id': self.channel.id})
        self.client.force_authenticate(user=self.user)
        self.data = {
            'name': "Updated Channel",
            'user': self.user.id,
            'description': "Updated description"
        }

    def tearDown(self):
        for file in ChannelFactory.files:
            if os.path.exists(file.path):
                os.remove(file.path)
        ChannelFactory.files.clear()

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put(self):
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
