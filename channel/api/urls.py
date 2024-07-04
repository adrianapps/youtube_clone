from django.urls import path

from .views import ChannelList, ChannelDetail, UserRegister, UserList, UserDetail

urlpatterns = [
    path('register/', UserRegister.as_view(), name='register'),
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:user_id>/', UserDetail.as_view(), name='user-detail'),
    path('users/<int:user_id>/channels/', ChannelList.as_view(), name='channel-list'),
    path('channels/', ChannelList.as_view(), name='channel-list'),
    path('channels/<int:channel_id>/', ChannelDetail.as_view(), name='channel-detail'),
]
