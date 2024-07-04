from rest_framework import generics
from rest_framework import permissions

from video.models import Video, Tag, WatchLater, Comment
from .serializers import VideoSerializer, TagSerializer, CommentSerializer, WatchLaterSerializer
from .permissions import IsVideoOwnerOrReadOnly, IsSuperUserOrReadOnly, IsWatchLaterOwner, IsCommentOwnerOrReadOnly


class TagList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperUserOrReadOnly]


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperUserOrReadOnly]
    lookup_url_kwarg = 'tag_id'


class VideoList(generics.ListCreateAPIView):
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        channel_id = self.kwargs.get('channel_id')
        queryset = Video.objects.select_related('channel').prefetch_related(
            'tag', 'likes', 'dislikes'
        )
        if channel_id:
            return queryset.filter(channel__id=channel_id)
        return queryset


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

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return WatchLater.objects.select_related('user').filter(user__id=user_id)


class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

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

