from django.urls import reverse
from django.test import TestCase

from channel.tests.factories import UserFactory, ChannelFactory
from video.models import Video
from video.tests.factories import TagFactory, VideoFactory, CommentFactory, WatchLaterFactory


class TagModelTest(TestCase):
    def setUp(self):
        self.tag = TagFactory()

    def test_tag_creation(self):
        self.assertEqual(str(self.tag), self.tag.name)


class VideoModelTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.likers = UserFactory.create_batch(3)
        self.dislikers = UserFactory.create_batch(3)
        self.channel = ChannelFactory(user=self.user)
        self.video = VideoFactory(user=self.user, channel=self.channel, likes=self.likers, dislikes=self.dislikers)
        self.comment = CommentFactory(user=self.user, video=self.video)

    def test_channel_creation(self):
        self.assertEqual(self.video.user, self.user)
        self.assertEqual(self.video.channel, self.channel)
        self.assertEqual(str(self.video), self.video.title)

    def test_save(self):
        video = VideoFactory(user=self.user, channel=self.channel, thumbnail=None)
        video.save()
        self.assertEqual(video.thumbnail, Video.DEFAULT_THUMBNAIL)

    def test_absolute_url(self):
        self.assertEqual(
            self.video.get_absolute_url(),
            reverse('video:video-detail', kwargs={'pk': self.video.pk})
        )

    def test_update_url(self):
        self.assertEqual(
            self.video.get_update_url(),
            reverse('video:video-update', kwargs={'pk': self.video.pk})
        )

    def test_delete_url(self):
        self.assertEqual(
            self.video.get_delete_url(),
            reverse('video:video-delete', kwargs={'pk': self.video.pk})
        )

    def test_like_count(self):
        self.assertEqual(self.video.like_count(), 3)

    def test_dislike_count(self):
        self.assertEqual(self.video.dislike_count(), 3)

    def test_like_status(self):
        self.assertTrue(self.video.like_status(self.likers[0]))
        self.assertFalse(self.video.like_status(self.dislikers[0]))

    def test_dislike_status(self):
        self.assertTrue(self.video.dislike_status(self.dislikers[0]))
        self.assertFalse(self.video.dislike_status(self.likers[0]))

    def test_comment_count(self):
        self.assertEqual(self.video.comment_count(), 1)


class CommentModelTest(TestCase):
    def setUp(self):
        self.channel_owner = UserFactory()
        self.channel = ChannelFactory(user=self.channel_owner)
        self.video = VideoFactory(user=self.channel_owner, channel=self.channel)
        self.commenter = UserFactory()
        self.comment = CommentFactory(user=self.commenter, video=self.video)

    def test_comment_creation(self):
        str_comment = f"{self.commenter} -- {self.video}"
        self.assertEqual(str(self.comment), str_comment)


class WatchLaterModelTest(TestCase):
    def setUp(self):
        self.channel_owner = UserFactory()
        self.channel = ChannelFactory(user=self.channel_owner)
        self.video = VideoFactory(user=self.channel_owner, channel=self.channel)
        self.viewer = UserFactory()
        self.watch_later = WatchLaterFactory(user=self.viewer, video=self.video)

    def test_watch_later_creation(self):
        self.assertEqual(self.watch_later.user, self.viewer)
        self.assertEqual(self.watch_later.video, self.video)
        str_watch_later = f"{self.viewer} -- {self.video}"
        self.assertEqual(str(self.watch_later), str_watch_later)
