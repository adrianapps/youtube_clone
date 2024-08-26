from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from video.models import Video
from .models import Channel
from .forms import RegisterForm, ChannelForm


def log_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('video:home')
        else:
            return redirect('channel:login')
    else:
        return render(request, 'channel/login.html')


def register(request):
    form = RegisterForm

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('channel:login')

    return render(request, 'channel/register.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect('video:home')


@login_required
def my_channels(request):
    channel_list = Channel.objects.filter(user=request.user).order_by('-subscribers')
    paginator = Paginator(channel_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'channel/my_channels.html', context)


def get_channel(request, pk):
    channel = get_object_or_404(Channel, pk=pk)
    video_list = Video.objects.filter(channel_id=pk).order_by('-upload_date')
    paginator = Paginator(video_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'channel': channel,
        'page_obj': page_obj
    }
    return channel, context


def channel_detail(request, pk):
    channel, context = get_channel(request, pk)
    if request.user == channel.user:
        return redirect('channel:creator-channel-detail', pk=pk)
    context['subscription_status'] = channel.subscription_status(request.user)

    return render(request, 'channel/channel_detail.html', context)


def creator_channel_detail(request, pk):
    channel, context = get_channel(request, pk)
    if request.user != channel.user:
        return redirect(channel.get_absolute_url())

    return render(request, 'channel/creator_channel_detail.html', context)


@login_required
def channel_create(request):
    form = ChannelForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect(form.instance.get_absolute_url())

    return render(request, 'channel/channel_create.html', {'form': form})


def channel_update(request, pk):
    channel = get_object_or_404(Channel, pk=pk)
    if request.user != channel.user:
        raise Http404('Unable to update channel, you are not the creator')

    form = ChannelForm(request.POST or None, request.FILES or None, instance=channel)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect(form.instance.get_absolute_url())
    return render(request, 'channel/channel_update.html', {'form': form})


def channel_delete(request, pk):
    channel = get_object_or_404(Channel, pk=pk)
    if request.user != channel.user:
        raise Http404('Unable to delete this channel, you are not the creator')
    channel.delete()
    return redirect('channel:my-channels')


@login_required
def subscribe(request, pk):
    channel = get_object_or_404(Channel, pk=pk)
    if request.user == channel.user:
        return redirect(channel.get_absolute_url())

    if channel.subscribers.filter(id=request.user.id).exists():
        channel.subscribers.remove(request.user)
    else:
        channel.subscribers.add(request.user)
    return redirect(channel.get_absolute_url())


@login_required
def my_subscriptions(request):
    video_list = Video.objects.filter(channel__subscribers=request.user).order_by('-upload_date')
    paginator = Paginator(video_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'channel/subscriptions.html', {'page_obj': page_obj})

