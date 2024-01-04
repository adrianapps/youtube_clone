from rest_framework.reverse import reverse

from channel.models import User
from rest_framework import serializers
from channel.models import Channel
from video.models import Video, Tag, WatchLater, Comment


class BaseSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    def get_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse('api:channel-detail', kwargs={'pk': obj.pk}, request=request)


class ChannelSerializer(BaseSerializer):
    class Meta:
        model = Channel
        fields = [
            'url',
            'id',
            'name',
            'user',
            'description',
            'subscribers',
            'avatar',
            'creation_date'
        ]
        read_only_fields = ['subscribers']


class UserSerializer(BaseSerializer):
    channels = ChannelSerializer(many=True, read_only=True, source='channel_set')

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'channels']


class VideoSerializer(BaseSerializer):
    class Meta:
        model = Video
        fields = [
            'url',
            'id',
            'title',
            'user',
            'description',
            'file',
            'upload_date'
        ]
        read_only_fields = ['upload_date', 'views', 'likes', 'dislikes']


class TagSerializer(BaseSerializer):
    class Meta:
        model = Tag
        fields = ['url', 'id', 'name']


class WatchLaterSerializer(BaseSerializer):

    class Meta:
        model = WatchLater
        fields = ['url', 'id', 'user', 'video', 'timestamp']
        read_only_fields = ['timestamp']


class CommentSerializer(BaseSerializer):

    class Meta:
        model = Comment
        fields = ['url', 'id', 'user', 'video', 'content', 'timestamp']
        read_only_fields = ['timestamp']
