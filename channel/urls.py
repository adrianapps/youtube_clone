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
    path('channel/<int:pk>', views.channel_detail, name='channel-detail')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
