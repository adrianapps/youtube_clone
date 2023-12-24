from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
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
            return redirect('login')
    else:
        return render(request, 'channel/login.html')


def register(request):
    form = RegisterForm

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    return render(request, 'channel/register.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect('video:home')
