from django.contrib.auth.decorators import login_required
from django.db.models import F, Q
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Video, WatchLater
from .forms import CommentForm, VideoForm


def home(request):
    video_list = Video.objects.order_by('upload_date')
    paginator = Paginator(video_list, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
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

    like_status = video.like_status(request.user)
    dislike_status = video.dislike_status(request.user)

    if request.user.is_authenticated:
        watch_later_status = WatchLater.objects.filter(user=request.user, video=video).exists()
    else:
        watch_later_status = False

    context = {
        'video': video,
        'form': form,
        'comment_list': comment_list,
        'like_status': like_status,
        'dislike_status': dislike_status,
        'watch_later_status': watch_later_status
    }

    return render(request, 'video/video.html', context)


@login_required
def add_video(request):
    form = VideoForm(request.user)
    if request.method == 'POST':
        form = VideoForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            new_video = form.save(commit=False)
            new_video.user = request.user
            new_video.save()
            return redirect(new_video.get_absolute_url())

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


@login_required
def video_update(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if video.user != request.user:
        raise Http404('Unable to update this video, you are not the creator')

    form = VideoForm(request.user, request.POST or None, request.FILES or None, instance=video)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect(form.instance.get_absolute_url())

    return render(request, 'video/update_video.html', {'form': form})


@login_required
def video_delete(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if video.user != request.user:
        raise Http404('Unable to delete this video, you are not the creator')
    video.delete()
    return redirect('video:home')


def toggle_like(request, video, is_like):
    if is_like:
        active_set = video.likes
        inactive_set = video.dislikes
    else:
        active_set = video.dislikes
        inactive_set = video.likes

    if active_set.filter(id=request.user.id).exists():
        active_set.remove(request.user)
    else:
        active_set.add(request.user)
        if inactive_set.filter(id=request.user.id).exists():
            inactive_set.remove(request.user)

    return redirect(video.get_absolute_url())


@login_required
def like(request, pk):
    video = get_object_or_404(Video, pk=pk)

    return toggle_like(request, video, True)


@login_required
def dislike(request, pk):
    video = get_object_or_404(Video, pk=pk)

    return toggle_like(request, video, False)


@login_required
def watch_later(request, pk):
    video = get_object_or_404(Video, pk=pk)
    obj, created = WatchLater.objects.get_or_create(user=request.user, video=video)
    if not created:
        obj.delete()
    return redirect(video.get_absolute_url())


@login_required
def my_watch_later(request):
    video_list = WatchLater.objects.filter(user=request.user).order_by('-timestamp')
    paginator = Paginator(video_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'video/my_watch_later.html', {'page_obj': page_obj})
