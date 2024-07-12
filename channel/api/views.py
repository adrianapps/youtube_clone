from django.db.models import Count
from rest_framework import generics
from rest_framework import permissions
from rest_framework.permissions import AllowAny
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from channel.models import Channel, User
from .serializers import UserPublicSerializer, UserPrivateSerializer, ChannelListSerializer, ChannelDetailSerializer
from .permissions import IsChannelOwnerOrReadOnly
from .filters import UserFilter, ChannelFilter


class UserRegister(generics.CreateAPIView):
    serializer_class = UserPrivateSerializer
    permission_classes = [AllowAny]


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserPublicSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = UserFilter


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserPublicSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'channel_id'


class ChannelList(generics.ListCreateAPIView):
    serializer_class = ChannelListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ChannelFilter
    ordering_fields = ['subscriber_count', 'creation_date']

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        queryset = Channel.objects.select_related('user').annotate(
            subscriber_count=Count('subscribers'))
        if user_id:
            return queryset.filter(user__id=user_id)
        return queryset


class ChannelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Channel.objects.prefetch_related('subscribers').select_related('user')
    serializer_class = ChannelDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsChannelOwnerOrReadOnly]
    lookup_url_kwarg = 'channel_id'
