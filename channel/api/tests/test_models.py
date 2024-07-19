from django.test import TestCase

from .factories import UserFactory, ChannelFactory

from channel.models import Channel


class ChannelModelTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.subscriber = UserFactory()
        self.channel = ChannelFactory(user=self.user)
        self.channel.subscribers.add(self.subscriber)

    def test_channel_creation(self):
        self.assertEqual(self.channel.user, self.user)
        self.assertEqual(str(self.channel), self.channel.name)

    def test_save(self):
        channel = ChannelFactory(user=self.user, avatar=None)
        channel.save()
        self.assertEqual(channel.avatar, Channel.DEFAULT_AVATAR)

    def test_subscriber_count(self):
        self.assertEqual(self.channel.subscriber_count(), 1)

    def test_subscription_status(self):
        self.assertEqual(self.channel.subscription_status(self.user), False)
        self.assertEqual(self.channel.subscription_status(self.subscriber), True)
