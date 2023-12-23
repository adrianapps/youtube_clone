from django.contrib.auth.decorators import login_required
from django.db.models import F, Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Video
from .forms import CommentForm, VideoForm


def home(request):
    video_list = Video.objects.all()

    context = {
        'video_list': video_list
    }
    return render(request, 'video/home.html', context)


def video_detail(request, pk):
    video = get_object_or_404(Video, pk=pk)
    Video.objects.filter(pk=pk).update(views=F('views') + 1)
    form = CommentForm()
    comment_list = video.comments.order_by('-timestamp')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.video = video
            new_comment.user = request.user
            new_comment.save()

    context = {
        'video': video,
        'form': form,
        'comment_list': comment_list
    }

    return render(request, 'video/video.html', context)


@login_required
def add_video(request):
    form = VideoForm()
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            new_video = form.save(commit=False)
            new_video.user = request.user
            new_video.save()
            return redirect('video:video-detail', pk=new_video.id)

    return render(request, 'video/add_video.html', {'form': form})


def search(request):
    query = request.GET.get('q', None)
    video_list = Video.objects.all()
    if query is not None:
        video_list = video_list.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )
    context = {
        'video_list': video_list,
        'query': query
    }
    return render(request, 'video/search.html', context)
