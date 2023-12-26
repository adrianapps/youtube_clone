from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'video'

urlpatterns = [
    path('', views.home, name='home'),
    path('video/<int:pk>', views.video_detail, name='video-detail'),
    path('add_video/', views.add_video, name='add-video'),
    path('video_update/<int:pk>', views.video_update, name='vide-update'),
    path('video_delete/<int:pk>', views.video_delete, name='video-delete'),
    path('search/', views.search, name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)