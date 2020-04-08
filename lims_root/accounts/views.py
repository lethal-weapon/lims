from django.contrib.auth import logout
from django.shortcuts import redirect, render


def forgot_view(request):
    return redirect('/')


def logout_view(request):
    logout(request)
    return redirect('/')


def login_view(request):
    return render(request, 'accounts/login.html', {})


def register_view(request):
    return render(request, 'accounts/register.html', {})
