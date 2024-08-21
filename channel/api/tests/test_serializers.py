from django.test import TestCase

from channel.api.serializers import UserPrivateSerializer, UserPublicSerializer, ChannelListSerializer, \
    ChannelDetailSerializer
from .factories import UserFactory, ChannelFactory


class UserPrivateSerializerTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.serializer = UserPrivateSerializer(instance=self.user)
        self.data = self.serializer.data

    def test_contains_expected_fields(self):
        self.assertEqual(set(self.data.keys()), {'email', 'username', 'password'})

    def test_email_field_content(self):
        self.assertEqual(self.data['email'], self.user.email)

    def test_username_field_content(self):
        self.assertEqual(self.data['username'], self.user.username)

    def test_password_field_content(self):
        self.assertEqual(self.data['password'], self.user.password)


class UserPublicSerializerTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.serializer = UserPublicSerializer(instance=self.user)
        self.data = self.serializer.data

    def test_contains_expected_fields(self):
        self.assertEqual(set(self.data.keys()), {'id', 'username'})

    def test_id_field_content(self):
        self.assertEqual(self.data['id'], self.user.id)

    def test_username_field_content(self):
        self.assertEqual(self.data['username'], self.user.username)


class ChannelListSerializerTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.channel = ChannelFactory(user=self.user)
        self.serializer = ChannelListSerializer(instance=self.channel)
        self.data = self.serializer.data

    def test_contain_expected_fields(self):
        expected_fields = {
            'id', 'name', 'user', 'description', 'creation_date', 'avatar'
        }
        self.assertEqual(set(self.data.keys()), expected_fields)

    def test_id_field_content(self):
        self.assertEqual(self.data['id'], self.channel.id)

    def test_name_field_content(self):
        self.assertEqual(self.data['name'], self.channel.name)

    def test_user_field_content(self):
        self.assertEqual(self.data['user'], self.channel.user.id)

    def test_description_field_content(self):
        self.assertEqual(self.data['description'], self.channel.description)

    def test_creation_date_field_content(self):
        formatted_creation_date = self.channel.creation_date.isoformat().replace('+00:00', 'Z')
        self.assertEqual(self.data['creation_date'], formatted_creation_date)

    def test_avatar_field_content(self):
        self.assertEqual(self.data['avatar'], self.channel.avatar.url)


class ChannelDetailSerializerTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.subscribers = UserFactory.create_batch(3)
        self.channel = ChannelFactory(user=self.user, subscribers=self.subscribers)
        self.serializer = ChannelDetailSerializer(instance=self.channel)
        self.data = self.serializer.data

    def test_contain_expected_fields(self):
        expected_fields = {
            'id', 'name', 'user', 'description',
            'subscribers', 'creation_date', 'avatar'
        }
        self.assertEqual(set(self.data.keys()), expected_fields)

    def test_id_field_content(self):
        self.assertEqual(self.data['id'], self.channel.id)

    def test_name_field_content(self):
        self.assertEqual(self.data['name'], self.channel.name)

    def test_user_field_content(self):
        self.assertEqual(self.data['user'], self.channel.user.id)

    def test_description_field_content(self):
        self.assertEqual(self.data['description'], self.channel.description)

    def test_subscribers_field_content(self):
        expected_subscribers_id = sorted([subscriber.id for subscriber in self.subscribers])
        self.assertEqual(self.data['subscribers'], expected_subscribers_id)

    def test_creation_date_field_content(self):
        formatted_creation_date = self.channel.creation_date.isoformat().replace('+00:00', 'Z')
        self.assertEqual(self.data['creation_date'], formatted_creation_date)

    def test_avatar_field_content(self):
        self.assertEqual(self.data['avatar'], self.channel.avatar.url)
