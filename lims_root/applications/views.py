from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy


@login_required(login_url=reverse_lazy('login'))
def my_list(request):
    return render(request, 'applications/my-list.html', {
    })


@login_required(login_url=reverse_lazy('login'))
def apply_facility(request):
    return render(request, 'applications/apply-facility.html', {
    })


@login_required(login_url=reverse_lazy('login'))
def apply_research(request):
    return render(request, 'applications/apply-research.html', {
    })
