from rest_framework import generics
from rest_framework import permissions
from rest_framework.permissions import AllowAny

from channel.models import Channel, User
from .serializers import UserPublicSerializer, UserPrivateSerializer, ChannelListSerializer, ChannelDetailSerializer
from .permissions import IsChannelOwnerOrReadOnly


class UserRegister(generics.CreateAPIView):
    serializer_class = UserPrivateSerializer
    permission_classes = [AllowAny]


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserPublicSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserPublicSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'channel_id'


class ChannelList(generics.ListCreateAPIView):
    serializer_class = ChannelListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if user_id:
            return Channel.objects.select_related('user').filter(user__id=user_id)
        return Channel.objects.select_related('user')


class ChannelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Channel.objects.prefetch_related('subscribers').select_related('user')
    serializer_class = ChannelDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsChannelOwnerOrReadOnly]
    lookup_url_kwarg = 'channel_id'
