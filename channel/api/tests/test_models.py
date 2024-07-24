import os
from django.test import TestCase

from youtube_clone.settings import MEDIA_ROOT
from channel.models import Channel
from .factories import UserFactory, ChannelFactory


class ChannelModelTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.subscribers = UserFactory.create_batch(3)
        self.channel = ChannelFactory(user=self.user, subscribers=self.subscribers)

    def tearDown(self):
        default_avatar_path = os.path.join(MEDIA_ROOT, 'avatars', 'default_avatar.jpg')
        for file in ChannelFactory.files:
            if os.path.exists(file.path) and file.path != default_avatar_path:
                os.remove(file.path)
        ChannelFactory.files.clear()

    def test_channel_creation(self):
        self.assertEqual(self.channel.user, self.user)
        self.assertEqual(str(self.channel), self.channel.name)

    def test_save(self):
        channel = ChannelFactory(user=self.user, avatar=None)
        channel.save()
        self.assertEqual(channel.avatar, Channel.DEFAULT_AVATAR)

    def test_subscriber_count(self):
        self.assertEqual(self.channel.subscriber_count(), 3)

    def test_subscription_status(self):
        self.assertEqual(self.channel.subscription_status(self.user), False)
        self.assertEqual(self.channel.subscription_status(self.subscribers[0]), True)
