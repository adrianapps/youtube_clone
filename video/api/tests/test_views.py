from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from channel.api.tests.factories import UserFactory
from video.api.tests.factories import TagFactory, VideoFactory, CommentFactory, WatchLaterFactory


class TagListTest(APITestCase):
    def setUp(self):
        self.url = reverse('api_video:tag-list')
        self.user = UserFactory()
        self.staff = UserFactory(is_staff=True)
        self.tag = TagFactory()
        self.client.force_authenticate(user=self.user)
        self.data = {'name': 'tag name'}

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_privileged(self):
        self.client.force_authenticate(user=self.staff)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_unprivileged(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TagDetailTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.staff = UserFactory(is_staff=True)
        self.tag = TagFactory()
        self.url = reverse('api_video:tag-detail', kwargs={'tag_id': self.tag.id})
        self.client.force_authenticate(user=self.user)
        self.data = {'name': 'updated tag name'}

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_privileged(self):
        self.client.force_authenticate(user=self.staff)
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_unprivileged(self):
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_privileged(self):
        self.client.force_authenticate(user=self.staff)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_unprivileged(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
