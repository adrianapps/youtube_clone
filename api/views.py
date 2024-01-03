from rest_framework import permissions, generics
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from channel.models import User, Channel
from video.models import Video, Tag, WatchLater
from .serializers import UserSerializer, ChannelSerializer, VideoSerializer, TagSerializer, WatchLaterSerializer
from .permissions import IsOwnerOrReadOnly


class UserListAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [DjangoModelPermissions]


class UserDetailAPIView(IsOwnerOrReadOnly, generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrReadOnly]


class ChannelListAPIView(generics.ListCreateAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = [DjangoModelPermissions]


class ChannelDetailAPIView(IsOwnerOrReadOnly, generics.RetrieveUpdateDestroyAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = [IsOwnerOrReadOnly]


class VideoListAPIView(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [DjangoModelPermissions]


class VideoDetailAPIView(IsOwnerOrReadOnly, generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsOwnerOrReadOnly]


class TagListAPIView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [DjangoModelPermissions]


class TagDetailAPIView(generics.RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [DjangoModelPermissions]


class WatchLaterListAPIView(generics.ListCreateAPIView):
    queryset = WatchLater.objects.all()
    serializer_class = WatchLaterSerializer
    permission_classes = [DjangoModelPermissions]


class WatchLaterDetailAPIView(IsOwnerOrReadOnly, generics.RetrieveUpdateDestroyAPIView):
    queryset = WatchLater.objects.all()
    serializer_class = WatchLaterSerializer
    permission_classes = [IsOwnerOrReadOnly]
