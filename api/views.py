from rest_framework import permissions, generics, viewsets, authentication
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from channel.models import User, Channel
from video.models import Video, Tag, WatchLater, Comment
from .serializers import UserSerializer, ChannelSerializer, VideoSerializer, TagSerializer, WatchLaterSerializer, \
    CommentSerializer
from .permissions import IsOwnerOrReadOnly


# @api_view(['GET'])
# def api_root(request, format=None):
#     return Response({
#         'user': reverse('api:user-list', request=request, format=format),
#         'channel': reverse('api:channel-list', request=request, format=format),
#         'video': reverse('api:video-list', request=request, format=format),
#         'tag': reverse('api:tag-list', request=request, format=format),
#         'watch_later': reverse('api:watchlater-list', request=request, format=format),
#         'comment': reverse('api:comment-list', request=request, format=format),
#     })
#

# class UserListAPIView(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [DjangoModelPermissions]
#
#
# class UserDetailAPIView(IsOwnerOrReadOnly, generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsOwnerOrReadOnly]
#
#
# class ChannelListAPIView(generics.ListCreateAPIView):
#     queryset = Channel.objects.all()
#     serializer_class = ChannelSerializer
#     permission_classes = [DjangoModelPermissions]
#
#
# class ChannelDetailAPIView(IsOwnerOrReadOnly, generics.RetrieveUpdateDestroyAPIView):
#     queryset = Channel.objects.all()
#     serializer_class = ChannelSerializer
#     permission_classes = [IsOwnerOrReadOnly]
#
#
# class VideoListAPIView(generics.ListCreateAPIView):
#     queryset = Video.objects.all()
#     serializer_class = VideoSerializer
#     permission_classes = [DjangoModelPermissions]
#
#
# class VideoDetailAPIView(IsOwnerOrReadOnly, generics.RetrieveUpdateDestroyAPIView):
#     queryset = Video.objects.all()
#     serializer_class = VideoSerializer
#     permission_classes = [IsOwnerOrReadOnly]
#
#
# class TagListAPIView(generics.ListCreateAPIView):
#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer
#     permission_classes = [DjangoModelPermissions]
#
#
# class TagDetailAPIView(generics.RetrieveAPIView):
#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer
#     permission_classes = [DjangoModelPermissions]
#
#
# class WatchLaterListAPIView(generics.ListCreateAPIView):
#     queryset = WatchLater.objects.all()
#     serializer_class = WatchLaterSerializer
#     permission_classes = [DjangoModelPermissions]
#
#
# class WatchLaterDetailAPIView(IsOwnerOrReadOnly, generics.RetrieveUpdateDestroyAPIView):
#     queryset = WatchLater.objects.all()
#     serializer_class = WatchLaterSerializer
#     permission_classes = [IsOwnerOrReadOnly]
#
#
# class CommentListAPIView(generics.ListCreateAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [DjangoModelPermissions]
#
#
# class CommentDetailAPIView(IsOwnerOrReadOnly, generics.RetrieveUpdateDestroyAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [IsOwnerOrReadOnly]


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class VideoViewSet(viewsets.ModelViewSet):
    serializer_class = VideoSerializer
    queryset = Video.objects.all()
    authentication_classes = [authentication.TokenAuthentication]

    def get_permissions(self):
        if self.action in ['destroy', 'update', 'partial_update']:
            permission_classes = [IsOwnerOrReadOnly]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]


class ChannelViewSet(viewsets.ModelViewSet):
    serializer_class = ChannelSerializer
    queryset = Channel.objects.all()


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class WatchLaterViewSet(viewsets.ModelViewSet):
    serializer_class = WatchLaterSerializer
    queryset = WatchLater.objects.all()
