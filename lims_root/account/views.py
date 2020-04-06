from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout


def logout_view(request):
    logout(request)
    return redirect('/')


def login_view(request):
    return render(request, 'account/login.html', {})


def register_view(request):
    return render(request, 'account/register.html', {})
