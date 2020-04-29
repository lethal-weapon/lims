from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy

from applications.models import FacilityApplication
from .models import Apparatus, Facility, Laboratory


# Only authenticated and verified users can view the inventory
@login_required(login_url=reverse_lazy('login'))
def warehouse(request):
    # Find out what facilities are unavailable
    fapps = FacilityApplication.objects.filter(status__in=['WAI', 'BOR', 'OVE'])
    in_use_facility_ids = []

    for fapp in fapps:
        for f in fapp.items.all():
            in_use_facility_ids.append(f.id)

    return render(request, 'inventory/warehouse.html', {
        'facility_list'            : Facility.objects.exclude(id__in=in_use_facility_ids),
        'apparatus_list'           : Apparatus.objects.exclude(id__in=in_use_facility_ids),
        'laboratory_list'          : Laboratory.objects.exclude(id__in=in_use_facility_ids),
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
    pass