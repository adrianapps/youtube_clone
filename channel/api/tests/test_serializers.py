from rest_framework.test import APITestCase

from channel.api.serializers import UserPrivateSerializer, UserPublicSerializer, ChannelListSerializer, \
    ChannelDetailSerializer
from channel.models import User, Channel
from .factories import UserFactory, ChannelFactory


class UserPrivateSerializerTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.serializer = UserPrivateSerializer(instance=self.user)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['email', 'username', 'password']))

    def test_email_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['email'], self.user.email)

    def test_username_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['username'], self.user.username)

    def test_password_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['password'], self.user.password)


class UserPublicSerializerTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.serializer = UserPublicSerializer(instance=self.user)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'username']))

    def test_id_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['id'], self.user.id)

    def test_username_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['username'], self.user.username)


class ChannelListSerializerTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.channel = ChannelFactory(user=self.user)
        self.serializer = ChannelListSerializer(instance=self.channel)

    def test_contain_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(
            ['id', 'name', 'user', 'description', 'creation_date', 'avatar']
        ))

    def test_id_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['id'], self.channel.id)

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.channel.name)

    def test_user_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['user'], self.channel.user.id)

    def test_description_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['description'], self.channel.description)

    def test_creation_date_field_content(self):
        data = self.serializer.data
        formatted_creation_date = self.channel.creation_date.isoformat().replace('+00:00', 'Z')
        self.assertEqual(data['creation_date'], formatted_creation_date)

    def test_avatar_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['avatar'], self.channel.avatar.url)


class ChannelDetailSerializerTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.subscriber = UserFactory()
        self.channel = ChannelFactory(user=self.user)
        self.channel.subscribers.add(self.subscriber)
        self.serializer = ChannelDetailSerializer(instance=self.channel)

    def test_contain_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(
            ['id', 'name', 'user', 'description', 'subscribers', 'creation_date', 'avatar']
        ))

    def test_id_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['id'], self.channel.id)

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.channel.name)

    def test_user_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['user'], self.channel.user.id)

    def test_description_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['description'], self.channel.description)

    def test_subscribers_field_content(self):
        data = self.serializer.data
        expected_subscriber_id = [self.subscriber.id]
        self.assertEqual(data['subscribers'], expected_subscriber_id)

    def test_creation_date_field_content(self):
        data = self.serializer.data
        formatted_creation_date = self.channel.creation_date.isoformat().replace('+00:00', 'Z')
        self.assertEqual(data['creation_date'], formatted_creation_date)

    def test_avatar_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['avatar'], self.channel.avatar.url)
