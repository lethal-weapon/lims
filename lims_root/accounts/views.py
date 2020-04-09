from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import AccountAuthenticationForm


@login_required(login_url=reverse_lazy('login'))
def user_home(request):
    return render(request, 'accounts/home.html', {})


def forgot_view(request):
    return redirect('/')


def login_view(request):
    home_url = reverse_lazy('user-home')
    if request.user.is_authenticated:
        return redirect(home_url)

    form = AccountAuthenticationForm()
    if request.method == 'POST':
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            user = authenticate(campus_id=request.POST['campus_id'],
                                password=request.POST['password'])
            if user:
                login(request, user)
                return redirect(home_url)

    return render(request, 'accounts/login.html', {'login_form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


def register_view(request):
    return render(request, 'accounts/register.html', {})
