from channel.models import User
from rest_framework import serializers
from channel.models import Channel
from video.models import Video, Tag, WatchLater


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id', 'name', 'user', 'description', 'subscribers', 'avatar', 'creation_date']
        read_only_fields = ['subscribers']


class UserSerializer(serializers.ModelSerializer):
    channels = ChannelSerializer(many=True, read_only=True, source='channel_set')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'channels']


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'
        read_only_fields = ['views', 'likes', 'dislikes']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class WatchLaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchLater
        fields = '__all__'
