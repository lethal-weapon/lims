from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import AccountAuthenticationForm, RegistrationForm
from .models import Account


@login_required(login_url=reverse_lazy('login'))
def update_email(request):
    email = request.GET.get('email')
    replies = {
        'message'   : '',
        'is_success': False,
    }

    try:
        account = Account.objects \
            .exclude(id=request.user.id) \
            .get(email__iexact=email)
    except Account.DoesNotExist:
        # nobody is using this email
        user_account = Account.objects.get(id=request.user.id)
        user_account.email = email
        user_account.save()
        replies['message'] = 'Email Updated'
        replies['is_success'] = True
    else:
        # somebody is using this email
        replies['message'] = 'Email "%s" is already in use.' % email
    finally:
        return JsonResponse(replies)


@login_required(login_url=reverse_lazy('login'))
def user_logout(request):
    logout(request)
    return redirect('/')


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
