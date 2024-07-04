from rest_framework import serializers

from video.models import Video, Comment, Tag, WatchLater
from channel.models import User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class VideoSerializer(serializers.ModelSerializer):
    tag = TagSerializer(read_only=True, many=True)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Video
        fields = [
            'id',
            'title',
            'user',
            'channel',
            'file',
            'thumbnail',
            'description',
            'upload_date',
            'tag',
            'likes',
            'dislikes',
            'views',
        ]
        read_only_fields = ['likes', 'dislikes', 'views']

    def validate_channel(self, value):
        user = self.context.get('request').user
        if value.user != user:
            raise serializers.ValidationError(f"{user.username} is not the owner of {value.name}")
        return value


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = [
            'id',
            'video',
            'user',
            'content',
        ]
        read_only_fields = ['timestamp']


class WatchLaterSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = WatchLater
        fields = [
            'id',
            'user',
            'video',
        ]
        read_only_fields = ['timestamp']
