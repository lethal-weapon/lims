from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import AccountAuthenticationForm, AccountUpdateForm, RegistrationForm


@login_required(login_url=reverse_lazy('login'))
def user_home(request):
    if request.method == 'GET':
        return render(request, 'accounts/home.html', {})

    elif request.method == 'POST':
        form = AccountUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            form.initial = {"email": request.POST['email']}
            form.save()
            message = 'Email Updated'
        else:
            message = 'This Email is Unavailable'

        return render(request, 'accounts/home.html', {
            'account_update_message': message})


def user_forgot(request):
    return redirect('/')


def user_login(request):
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


def user_logout(request):
    logout(request)
    return redirect('/')


def user_register(request):
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            account = authenticate(
                campus_id=form.cleaned_data.get('campus_id'),
                password=form.cleaned_data.get('password1'))

            login(request, account)
            return redirect(reverse_lazy('register-success'))

    return render(request, 'accounts/register.html',
                  {'registration_form': form})
