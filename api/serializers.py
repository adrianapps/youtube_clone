from rest_framework.reverse import reverse

from channel.models import User
from rest_framework import serializers
from channel.models import Channel
from video.models import Video, Tag, WatchLater, Comment


class BaseSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    def get_url(self, obj):
        request = self.context.get('request')
        view_name = f'api:{self.Meta.model.__name__.lower()}-detail'
        if request is None:
            return None
        return reverse(view_name, kwargs={'pk': obj.pk}, request=request)

    class Meta:
        abstract = True


class ChannelSerializer(BaseSerializer):
    user_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Channel
        fields = [
            'url',
            'id',
            'name',
            'user',
            'user_url',
            'description',
            'subscribers',
            'avatar',
            'creation_date'
        ]
        read_only_fields = ['user', 'subscribers']

    def get_user_url(self, obj):
        if obj.user:
            return reverse('api:user-detail', kwargs={'pk': obj.user.pk}, request=self.context.get('request'))
        return None

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user:
            validated_data['user'] = request.user
        return super().create(validated_data)


class UserSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request', None)
        if request and request.user != instance:
            data.pop('email', None)
        return data


class VideoSerializer(BaseSerializer):
    channel_url = serializers.SerializerMethodField(read_only=True)
    user_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Video
        fields = [
            'url',
            'id',
            'title',
            'channel',
            'channel_url',
            'user',
            'user_url',
            'description',
            'file',
            'likes',
            'dislikes',
            'upload_date'
        ]
        read_only_fields = ['user', 'upload_date', 'views', 'likes', 'dislikes']

    def get_channel_url(self, obj):
        if obj.channel:
            return reverse('api:channel-detail', kwargs={'pk': obj.channel.pk}, request=self.context.get('request'))
        return None

    def get_user_url(self, obj):
        if obj.user:
            return reverse('api:user-detail', kwargs={'pk': obj.user.pk}, request=self.context.get('request'))
        return None

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user:
            validated_data['user'] = request.user
        return super().create(validated_data)

    def get_fields(self):
        fields = super().get_fields()
        user = self.context['request'].user

        if user.is_authenticated:
            fields['channel'] = serializers.PrimaryKeyRelatedField(
                queryset=Channel.objects.filter(user=user),
                write_only=True
            )
        return fields


class TagSerializer(BaseSerializer):
    class Meta:
        model = Tag
        fields = ['url', 'id', 'name']


class WatchLaterSerializer(BaseSerializer):
    user_url = serializers.SerializerMethodField(read_only=True)
    video_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = WatchLater
        fields = [
            'url',
            'id',
            'user',
            'user_url',
            'video',
            'video_url',
            'timestamp'
        ]
        read_only_fields = ['user', 'timestamp']

    def get_user_url(self, obj):
        if obj.user:
            return reverse('api:user-detail', kwargs={'pk': obj.user.pk}, request=self.context.get('request'))
        return None

    def get_video_url(self, obj):
        if obj.video:
            return reverse('api:video-detail', kwargs={'pk': obj.video.pk}, request=self.context.get('request'))
        return None

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user:
            validated_data['user'] = request.user
        return super().create(validated_data)


class CommentSerializer(BaseSerializer):
    user_url = serializers.SerializerMethodField(read_only=True)
    video_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'url',
            'id',
            'user',
            'user_url',
            'video',
            'video_url',
            'content',
            'timestamp'
        ]
        read_only_fields = ['user', 'timestamp']

    def get_user_url(self, obj):
        if obj.user:
            return reverse('api:user-detail', kwargs={'pk': obj.user.pk}, request=self.context.get('request'))
        return None

    def get_video_url(self, obj):
        if obj.video:
            return reverse('api:video-detail', kwargs={'pk': obj.video.pk}, request=self.context.get('request'))
        return None

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user:
            validated_data['user'] = request.user
        return super().create(validated_data)
