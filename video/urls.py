from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'video'

urlpatterns = [
    path('', views.home, name='home'),
    path('video/<int:pk>', views.video_detail, name='video-detail'),
    path('video/like/<int:pk>', views.like, name='like'),
    path('video/dislike/<int:pk>', views.dislike, name='dislike'),
    path('video/create', views.add_video, name='add-video'),
    path('video/update/<int:pk>', views.video_update, name='vide-update'),
    path('video/delete/<int:pk>', views.video_delete, name='video-delete'),
    path('search/', views.search, name='search'),
    path('video/watch_later/<int:pk>', views.watch_later, name='watch-later'),
    path('watch_later/', views.my_watch_later, name='my-watch-later'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)