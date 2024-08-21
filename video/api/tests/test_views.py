from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from channel.api.tests.factories import UserFactory, ChannelFactory
from video.api.tests.factories import TagFactory, VideoFactory, CommentFactory, WatchLaterFactory
from .utils import create_image_file


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


class VideoListTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.channel_owner = UserFactory()
        self.channel = ChannelFactory(user=self.channel_owner)
        self.video = VideoFactory(user=self.channel_owner, channel=self.channel)
        self.url = reverse('api_video:video-list')
        self.client.force_authenticate(user=self.user)

        self.mock_file = SimpleUploadedFile("test_video.mp4", b"file_content", content_type="video/mp4")
        self.mock_thumbnail = create_image_file('test_thumbnail.jpg')

        self.data = {
            'title': 'video title',
            'user': self.channel_owner.id,
            'channel': self.channel.id,
            'file': self.mock_file,
            'thumbnail': self.mock_thumbnail,
            'description': 'video description',
        }

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_privileged(self):
        self.client.force_authenticate(user=self.channel_owner)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_unprivileged(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ChannelVideoListTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.channel = ChannelFactory(user=self.user)
        self.video = VideoFactory(user=self.user, channel=self.channel)
        self.url = reverse('api_video:channel-videos', kwargs={'channel_id': self.channel.id})
        self.client.force_authenticate(user=self.user)

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class VideoDetailTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.channel_owner = UserFactory()
        self.channel = ChannelFactory(user=self.channel_owner)
        self.video = VideoFactory(user=self.channel_owner, channel=self.channel)
        self.url = reverse('api_video:video-detail', kwargs={'video_id': self.video.id})
        self.client.force_authenticate(user=self.user)

        self.mock_file = SimpleUploadedFile("test_video_updated.mp4", b"file_content", content_type="video/mp4")
        self.mock_thumbnail = create_image_file('test_thumbnail.jpg')

        self.data = {
            'title': 'video title updated',
            'user': self.channel_owner.id,
            'channel': self.channel.id,
            'file': self.mock_file,
            'thumbnail': self.mock_thumbnail,
            'description': 'video description updated',
        }

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_privileged(self):
        self.client.force_authenticate(user=self.channel_owner)
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_unprivileged(self):
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_privileged(self):
        self.client.force_authenticate(user=self.channel_owner)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_unprivileged(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class WatchLaterListTest(APITestCase):
    def setUp(self):
        self.owner = UserFactory()
        self.user = UserFactory()
        self.video = VideoFactory()
        self.watch_later = WatchLaterFactory(user=self.owner)
        self.url = reverse('api_video:watch-later-list', kwargs={'user_id': self.owner.id})
        self.client.force_authenticate(user=self.owner)

        self.data = {
            'user': self.owner.id,
            'video': self.video.id,
        }

    def test_get_privileged(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_unprivileged(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class WatchLaterDetailTest(APITestCase):
    def setUp(self):
        self.owner = UserFactory()
        self.user = UserFactory()
        self.watch_later = WatchLaterFactory(user=self.owner)
        self.url = reverse('api_video:watch-later-detail', kwargs={
            'user_id': self.owner.id,
            'watch_later_id': self.watch_later.id
        })
        self.client.force_authenticate(user=self.owner)

    def test_get_privileged(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_unprivileged(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_privileged(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_unprivileged(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CommentListTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.comment = CommentFactory()
        self.url = reverse('api_video:video-comments', kwargs={'video_id': self.comment.video.id})
        self.client.force_authenticate(self.user)

        self.data = {
            'user': self.user.id,
            'content': "test content",
            'video': self.comment.video.id
        }

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CommentDetailTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.commenter = UserFactory()
        self.comment = CommentFactory(user=self.commenter)
        self.url = reverse('api_video:comment-detail', kwargs={
            'video_id': self.comment.video.id,
            'comment_id': self.comment.id
        })
        self.client.force_authenticate(self.user)

        self.data = {
            'user': self.commenter.id,
            'content': "test content updated",
            'video': self.comment.video.id
        }

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_privileged(self):
        self.client.force_authenticate(self.commenter)
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_unprivileged(self):
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_privileged(self):
        self.client.force_authenticate(self.commenter)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_unprivileged(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
