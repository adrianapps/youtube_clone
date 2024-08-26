from django.test import TestCase

from video.api.serializers import TagSerializer, VideoSerializer, WatchLaterSerializer, CommentSerializer
from channel.tests.factories import UserFactory
from video.tests.factories import TagFactory, VideoFactory, WatchLaterFactory, CommentFactory


class TagSerializerTest(TestCase):
    def setUp(self):
        self.tag = TagFactory()
        self.serializer = TagSerializer(instance=self.tag)
        self.data = self.serializer.data

    def test_contains_expected_fields(self):
        self.assertEqual(set(self.data.keys()), {'id', 'name'})

    def test_id_field_content(self):
        self.assertEqual(self.data['id'], self.tag.id)

    def test_name_field_content(self):
        self.assertEqual(self.data['name'], self.tag.name)


class VideoSerializerTest(TestCase):
    def setUp(self):
        self.likes = UserFactory.create_batch(3)
        self.dislikes = UserFactory.create_batch(3)
        self.tags = TagFactory.create_batch(3)
        self.video = VideoFactory(likes=self.likes, dislikes=self.dislikes, tag=self.tags)
        self.serializer = VideoSerializer(instance=self.video)
        self.data = self.serializer.data

    def test_contains_expected_fields(self):
        expected_fields = {
            'id', 'title', 'user', 'channel', 'file', 'thumbnail',
            'description', 'upload_date', 'tag', 'likes', 'dislikes', 'views'
        }
        self.assertEqual(set(self.data.keys()), expected_fields)

    def test_id_field_content(self):
        self.assertEqual(self.data['id'], self.video.id)

    def test_title_field_content(self):
        self.assertEqual(self.data['title'], self.video.title)

    def test_user_field_content(self):
        self.assertEqual(self.data['user'], self.video.user.id)

    def test_channel_field_content(self):
        self.assertEqual(self.data['channel'], self.video.channel.id)

    def test_file_field_content(self):
        self.assertEqual(self.data['file'], self.video.file.url)

    def test_thumbnail_field_content(self):
        self.assertEqual(self.data['thumbnail'], self.video.thumbnail.url)

    def test_description_field_content(self):
        self.assertEqual(self.data['description'], self.video.description)

    def test_upload_date_field_content(self):
        formatted_upload_date = self.video.upload_date.isoformat().replace('+00:00', 'Z')
        self.assertEqual(self.data['upload_date'], formatted_upload_date)

    def test_tag_field_content(self):
        expected_tags_id = sorted([tag.id for tag in self.tags])
        self.assertEqual(sorted(self.data['tag']), expected_tags_id)

    def test_likes_field_content(self):
        expected_users_id = sorted([user.id for user in self.likes])
        self.assertEqual(sorted(self.data['likes']), expected_users_id)

    def test_dislikes_field_content(self):
        expected_users_id = sorted([user.id for user in self.dislikes])
        self.assertEqual(sorted(self.data['dislikes']), expected_users_id)

    def test_views_field_content(self):
        self.assertEqual(self.data['views'], self.video.views)


class CommentSerializerTest(TestCase):
    def setUp(self):
        self.comment = CommentFactory()
        self.serializer = CommentSerializer(instance=self.comment)
        self.data = self.serializer.data

    def test_contains_expected_fields(self):
        self.assertEqual(set(self.data.keys()), {'id', 'video', 'user', 'content', 'timestamp'})

    def test_id_field_content(self):
        self.assertEqual(self.data['id'], self.comment.id)

    def test_video_field_content(self):
        self.assertEqual(self.data['video'], self.comment.video.id)

    def test_user_field_content(self):
        self.assertEqual(self.data['user'], self.comment.user.id)

    def test_content_field_content(self):
        self.assertEqual(self.data['content'], self.comment.content)


class WatchLaterSerializerTest(TestCase):
    def setUp(self):
        self.watch_later = WatchLaterFactory()
        self.serializer = WatchLaterSerializer(instance=self.watch_later)
        self.data = self.serializer.data

    def test_contains_expected_fields(self):
        self.assertEqual(set(self.data.keys()), {'id', 'user', 'video', 'timestamp'})

    def test_id_field_content(self):
        self.assertEqual(self.data['id'], self.watch_later.id)

    def test_user_field_content(self):
        self.assertEqual(self.data['user'], self.watch_later.user.id)

    def test_video_field_content(self):
        self.assertEqual(self.data['video'], self.watch_later.video.id)

    def test_timestamp_field_content(self):
        formatted_timestamp = self.watch_later.timestamp.isoformat().replace('+00:00', 'Z')
        self.assertEqual(self.data['timestamp'], formatted_timestamp)
