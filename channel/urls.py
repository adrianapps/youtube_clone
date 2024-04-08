from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'channel'

urlpatterns = [
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('register/', views.register, name='register'),
    path('channel/', views.my_channels, name='my-channels'),
    path('channel/', views.channel_create, name='channel-create'),
    path('channel/<int:pk>/delete', views.channel_delete, name='channel-delete'),
    path('channel<int:pk>/update', views.channel_update, name='channel-update'),
    path('channel/<int:pk>', views.channel_detail, name='channel-detail'),
    path('channel/<int:pk>/creator', views.creator_channel_detail, name='creator-channel-detail'),
    path('subscribe/<int:pk>', views.subscribe, name='subscribe'),
    path('subscriptions/', views.my_subscriptions, name='my-subscriptions')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
