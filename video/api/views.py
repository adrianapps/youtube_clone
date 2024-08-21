from django.db.models import Count
from rest_framework import generics
from rest_framework import permissions
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from video.models import Video, Tag, WatchLater, Comment
from .serializers import VideoSerializer, TagSerializer, CommentSerializer, WatchLaterSerializer
from .permissions import IsVideoOwnerOrReadOnly, IsStaffOrReadOnly, IsWatchLaterOwner, IsCommentOwnerOrReadOnly
from .filters import TagFilter, VideoFilter, CommentFilter, WatchLaterFilter


class TagList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = TagFilter
    ordering_filters = ['name']


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffOrReadOnly]
    lookup_url_kwarg = 'tag_id'


class VideoList(generics.ListCreateAPIView):
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = VideoFilter
    ordering_filters = ['likes_count', 'dislikes_count', 'upload_date']

    def get_queryset(self):
        queryset = Video.objects.select_related('channel').prefetch_related(
            'tag', 'likes', 'dislikes'
        ).annotate(
            likes_count=Count('likes'),
            dislikes_count=Count('dislikes')
        )
        return queryset


class ChannelVideoList(generics.ListAPIView):
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = VideoFilter
    ordering_filters = ['likes_count', 'dislikes_count', 'upload_date']

    def get_queryset(self):
        queryset = Video.objects.select_related('channel').prefetch_related(
            'tag', 'likes', 'dislikes'
        ).annotate(
            likes_count=Count('likes'),
            dislikes_count=Count('dislikes')
        )
        channel_id = self.kwargs.get('channel_id')
        return queryset.filter(channel__id=channel_id)


class VideoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.select_related('channel').prefetch_related(
        'tag', 'likes', 'dislikes'
    )
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated, IsVideoOwnerOrReadOnly]
    lookup_url_kwarg = 'video_id'


class WatchLaterList(generics.ListCreateAPIView):
    serializer_class = WatchLaterSerializer
    permission_classes = [permissions.IsAuthenticated, IsWatchLaterOwner]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = WatchLaterFilter
    ordering_filters = ['timestamp', 'user__username', 'video__title']

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return WatchLater.objects.select_related('user').filter(user__id=user_id)


class WatchLaterDetail(generics.RetrieveDestroyAPIView):
    serializer_class = WatchLaterSerializer
    permission_classes = [permissions.IsAuthenticated, IsWatchLaterOwner]
    lookup_url_kwarg = 'watch_later_id'

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return WatchLater.objects.select_related('user').filter(user__id=user_id)


class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CommentFilter
    ordering_filters = ['timestamp', 'user__username', 'video__title']

    def get_queryset(self):
        video_id = self.kwargs.get('video_id')
        return Comment.objects.select_related('video', 'user').filter(video__id=video_id)

    def perform_create(self, serializer):
        video_id = self.kwargs.get('video_id')
        video = Video.objects.get(pk=video_id)
        serializer.save(video=video)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsCommentOwnerOrReadOnly]
    lookup_url_kwarg = 'comment_id'

    def get_queryset(self):
        video_id = self.kwargs.get('video_id')
        return Comment.objects.select_related('video', 'user').filter(video__id=video_id)
