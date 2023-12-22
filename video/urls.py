from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'video'

urlpatterns = [
    path('', views.home, name='home'),
    path('video/<int:pk>', views.video_detail, name='video'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)