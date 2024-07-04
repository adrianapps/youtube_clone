from django.urls import path

from .views import VideoList, VideoDetail, TagList, TagDetail, CommentList, CommentDetail

urlpatterns = [
    path('channels/<int:channel_id>/videos/', VideoList.as_view(), name='channel-videos'),
    path('videos/', VideoList.as_view(), name='video-list'),
    path('videos/<int:video_id>/', VideoDetail.as_view(), name='video-detail'),
    path('videos/<int:video_id>/comments/', CommentList.as_view(), name='video-comments'),
    path('videos/<int:video_id>/comments/<int:comment_id>/', CommentDetail.as_view(), name='comment-detail'),

    path('tags/', TagList.as_view(), name='tag-list'),
    path('tags/<int:tag_id>', TagDetail.as_view(), name='tag-detail'),
]
