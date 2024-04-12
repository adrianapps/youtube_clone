from rest_framework import viewsets

from channel.models import User, Channel
from video.models import Video, Tag, WatchLater, Comment
from .serializers import UserSerializer, ChannelSerializer, VideoSerializer, TagSerializer, WatchLaterSerializer, \
    CommentSerializer
from .mixins import IsOwnerOrReadOnlyMixin, IsUserOrReadOnlyMixin


class UserViewSet(IsUserOrReadOnlyMixin, viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class VideoViewSet(IsOwnerOrReadOnlyMixin, viewsets.ModelViewSet):
    serializer_class = VideoSerializer
    queryset = Video.objects.all()


class ChannelViewSet(IsOwnerOrReadOnlyMixin, viewsets.ModelViewSet):
    serializer_class = ChannelSerializer
    queryset = Channel.objects.all()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class CommentViewSet(IsOwnerOrReadOnlyMixin, viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class WatchLaterViewSet(IsOwnerOrReadOnlyMixin, viewsets.ModelViewSet):
    serializer_class = WatchLaterSerializer
    queryset = WatchLater.objects.all()
