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
    path('channel_create/', views.channel_create, name='channel-create'),
    path('channel_delete/<int:pk>', views.channel_delete, name='channel-delete'),
    path('channel_update/<int:pk>', views.channel_update, name='channel-update'),
    path('channel/<int:pk>', views.channel_detail, name='channel-detail')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
