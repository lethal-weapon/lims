from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy

from applications.models import FacilityApplication
from .models import Apparatus, Facility, Laboratory


# Find out what facilities are unavailable
def get_occupied_facilities():
    fapps = FacilityApplication.objects.filter(status__in=['WAI', 'BOR', 'OVE'])
    facilities = set()

    for fapp in fapps:
        for f in fapp.items.all():
            facilities.add(f)

    return facilities


# Only authenticated and verified users can view the inventory
@login_required(login_url=reverse_lazy('login'))
def warehouse(request):
    occupied_ids = set([f.id for f in get_occupied_facilities()])
    return render(request, 'inventory/warehouse.html', {
        'facility_list'            : Facility.objects.exclude(id__in=occupied_ids),
        'apparatus_list'           : Apparatus.objects.exclude(id__in=occupied_ids),
        'laboratory_list'          : Laboratory.objects.exclude(id__in=occupied_ids),
        'facility_application_list': FacilityApplication.objects.filter(
            applicant=request.user
        ).filter(
            status='PEN'
        ),
    })


# Add a facility to 'items' field of an
# application list whose status is PENDING
@login_required(login_url=reverse_lazy('login'))
def add_facility_to_list(request):
    f = Facility.objects.get(id=request.GET.get('facility_id'))
    fa = FacilityApplication.objects.get(id=request.GET.get('facility_app_id'))

    if f and fa:
        if fa.status == 'PEN' and (f not in fa.items.all()):
            fa.items.add(f)
            fa.save()
            return JsonResponse({'is_success': True})

    return JsonResponse({'is_success': False})
