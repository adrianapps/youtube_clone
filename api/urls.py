from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from . import views
from .views import UserViewSet, VideoViewSet, ChannelViewSet, TagViewSet, WatchLaterViewSet

app_name = 'api'

# urlpatterns = format_suffix_patterns([
#     path('', views.api_root),
#     path('user/', views.UserListAPIView.as_view(), name='user-list'),
#     path('user/<int:pk>', views.UserDetailAPIView.as_view(), name='user-detail'),
#     path('channel/', views.ChannelListAPIView.as_view(), name='channel-list'),
#     path('channel/<int:pk>', views.ChannelDetailAPIView.as_view(), name='channel-detail'),
#     path('video/', views.VideoListAPIView.as_view(), name='video-list'),
#     path('video/<int:pk>', views.VideoDetailAPIView.as_view(), name='video-detail'),
#     path('tag/', views.TagListAPIView.as_view(), name='tag-list'),
#     path('tag/<int:pk>', views.TagDetailAPIView.as_view(), name='tag-detail'),
#     path('watch_later/', views.WatchLaterListAPIView.as_view(), name='watchlater-list'),
#     path('watch_later/<int:pk>', views.WatchLaterDetailAPIView.as_view(), name='watchlater-detail'),
#     path('comment/', views.CommentListAPIView.as_view(), name='comment-list'),
#     path('comment/<int:pk>', views.CommentDetailAPIView.as_view(), name='comment-detail'),
# ])

router = DefaultRouter()
router.register('user', UserViewSet, basename='user')
router.register('video', VideoViewSet, basename='video')
router.register('channel', ChannelViewSet, basename='channel')
router.register('tag', TagViewSet, basename='tag')
router.register('watchlater', WatchLaterViewSet, basename='watchlater')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', obtain_auth_token)
]
