from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from video.models import Video
from .models import Channel
from .forms import RegisterForm


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


def channel_detail(request, pk):
    channel = get_object_or_404(Channel, pk=pk)
    video_list = Video.objects.filter(channel_id=pk)
    paginator = Paginator(video_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'channel': channel,
        'page_obj': page_obj
    }
    return render(request, 'channel/channel_detail.html', context)
