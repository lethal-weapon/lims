from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy

from .models import Apparatus, Laboratory


@login_required(login_url=reverse_lazy('login'))
def warehouse(request):
    # only authenticated and verified users can view the inventory
    return render(request, 'inventory/warehouse.html', {
        'apparatus_list' : Apparatus.objects.all(),
        'laboratory_list': Laboratory.objects.all(),
    })
