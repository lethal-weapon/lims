from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import AccountAuthenticationForm, AccountUpdateForm, RegistrationForm


# Update account info
@login_required(login_url=reverse_lazy('login'))
def user_home(request):
    if request.method == 'GET':
        return redirect(reverse_lazy('site-bulletin'))

    elif request.method == 'POST':
        context = {}
        form = AccountUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            form.initial = {"email": request.POST['email']}
            form.save()
            context['account_update_message'] = 'Email Updated'
        else:
            context['account_update_message'] = 'This Email is Unavailable'

        return render(request, 'accounts/home.html', context)


def user_forgot(request):
    return redirect('/')


def user_login(request, template_name='accounts/login.html'):
    bulletin_url = reverse_lazy('site-bulletin')
    if request.user.is_authenticated:
        return redirect(bulletin_url)

    form = AccountAuthenticationForm()
    if request.method == 'POST':
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            user = authenticate(campus_id=request.POST['campus_id'],
                                password=request.POST['password'])
            if user:
                login(request, user)
                return redirect(bulletin_url)

    return render(request, template_name, {'login_form': form})


@login_required(login_url=reverse_lazy('login'))
def user_logout(request):
    logout(request)
    return redirect('/')


def user_register(request, template_name='accounts/register.html'):
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

    return render(request, template_name, {'registration_form': form})
