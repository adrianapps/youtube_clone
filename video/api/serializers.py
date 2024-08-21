from rest_framework import serializers

from video.models import Video, Comment, Tag, WatchLater
from channel.models import User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class VideoSerializer(serializers.ModelSerializer):
    tag = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
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

    def update(self, instance, validated_data):
        validated_data.pop('file', None)
        return super().update(instance, validated_data)


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
            'timestamp',
        ]
        read_only_fields = ['timestamp']


class WatchLaterSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = WatchLater
        fields = [
            'id',
            'user',
            'video',
            'timestamp',
        ]
        read_only_fields = ['timestamp']
