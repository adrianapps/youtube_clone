from django.test import TestCase
from django.urls import reverse

from channel.models import Channel
from .factories import UserFactory, ChannelFactory


class ChannelModelTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.subscribers = UserFactory.create_batch(3)
        self.channel = ChannelFactory(user=self.user, subscribers=self.subscribers)

    def test_channel_creation(self):
        self.assertEqual(self.channel.user, self.user)
        self.assertEqual(str(self.channel), self.channel.name)

    def test_absolute_url(self):
        self.assertEqual(
            self.channel.get_absolute_url(),
            reverse('channel:channel-detail', kwargs={'pk': self.channel.pk})
        )

    def test_update_url(self):
        self.assertEqual(
            self.channel.get_update_url(),
            reverse('channel:channel-update', kwargs={'pk': self.channel.pk})
        )

    def test_delete_url(self):
        self.assertEqual(
            self.channel.get_delete_url(),
            reverse('channel:channel-delete', kwargs={'pk': self.channel.pk})
        )

    def test_save(self):
        channel = ChannelFactory(user=self.user, avatar=None)
        channel.save()
        self.assertEqual(channel.avatar, Channel.DEFAULT_AVATAR)

    def test_subscriber_count(self):
        self.assertEqual(self.channel.subscriber_count(), 3)

    def test_subscription_status(self):
        self.assertEqual(self.channel.subscription_status(self.user), False)
        self.assertEqual(self.channel.subscription_status(self.subscribers[0]), True)
