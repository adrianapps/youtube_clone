from django.db.models import F
from django.shortcuts import render, get_object_or_404
from .models import Video


def home(request):
    video_list = Video.objects.all()

    context = {
        'video_list': video_list
    }
    return render(request, 'video/home.html', context)

def video_detail(request, pk):
    video = get_object_or_404(Video, pk=pk)
    Video.objects.filter(pk=pk).update(views=F('views') + 1)

    context = {
        'video': video,
    }

    return render(request, 'video/video.html', context)