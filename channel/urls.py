from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('register/', views.register, name='register')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
