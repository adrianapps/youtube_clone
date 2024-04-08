from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'video'

urlpatterns = [
    path('', views.home, name='home'),
    path('video/<int:pk>', views.video_detail, name='video-detail'),
    path('video/<int:pk>/like', views.like, name='like'),
    path('video/<int:pk>/dislike', views.dislike, name='dislike'),
    path('video/create', views.add_video, name='add-video'),
    path('video/<int:pk>/update', views.video_update, name='video-update'),
    path('video/<int:pk>/delete', views.video_delete, name='video-delete'),
    path('search/', views.search, name='search'),
    path('video/<int:pk>/watch_later', views.watch_later, name='watch-later'),
    path('watch_later/', views.my_watch_later, name='my-watch-later'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)