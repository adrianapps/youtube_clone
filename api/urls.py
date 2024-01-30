from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, VideoViewSet, ChannelViewSet, TagViewSet, WatchLaterViewSet, CommentViewSet

app_name = 'api'

router = DefaultRouter()
router.register('user', UserViewSet, basename='user')
router.register('video', VideoViewSet, basename='video')
router.register('channel', ChannelViewSet, basename='channel')
router.register('tag', TagViewSet, basename='tag')
router.register('comment', CommentViewSet, basename='comment')
router.register('watch-later', WatchLaterViewSet, basename='watchlater')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', obtain_auth_token)
]
