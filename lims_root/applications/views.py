from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy

from inventory.models import Apparatus, Facility, Laboratory
from .forms import FacilityApplicationForm
from .models import FacilityApplication, ResearchApplication


@login_required(login_url=reverse_lazy('login'))
def my_list(request):
    fal = FacilityApplication.objects.filter(applicant=request.user)
    ral = ResearchApplication.objects.filter(applicant=request.user)
    apparatus_ids = [apparatus.id for apparatus in Apparatus.objects.all()]

    context = {}
    for fa in fal:
        context[fa] = {'apparatus_list': [], 'lab_list': []}
        for f in fa.items.all():
            if f.id in apparatus_ids:
                context[fa]['apparatus_list'].append(Apparatus.objects.get(id=f.id))
            else:
                context[fa]['lab_list'].append(Laboratory.objects.get(id=f.id))

    return render(request, 'applications/my-list.html', {
        'facility_application_list': fal,
        'research_application_list': ral,
        'context'                  : context,
    })


@login_required(login_url=reverse_lazy('login'))
def apply_facility(request):
    if request.method == 'GET':
        return render(request, 'applications/apply-facility.html')

    elif request.method == 'POST':
        form = FacilityApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            try:
                app.applicant = request.user
            except Exception:
                pass
            app.save()
            return render(request, 'applications/apply-facility.html', {
                'apply_message': 'Application Added',
                'is_success'   : True,
            })

        return render(request, 'applications/apply-facility.html', {
            'apply_message': 'Please Fill Fields with Reasonable Input',
            'is_success'   : False,
        })


@login_required(login_url=reverse_lazy('login'))
def apply_research(request):
    return render(request, 'applications/apply-research.html', {
    })


@login_required(login_url=reverse_lazy('login'))
def update_facility_application(request):
    data = request.GET
    fa = FacilityApplication.objects.get(id=data.get('id'))

    if len(data.get('alias')) > 0:
        fa.alias = data.get('alias')

    if fa.status == 'PEN':
        start, end, reason = data.get('start'), data.get('end'), data.get('reason')

        if len(start) > 0 and start > str(datetime.today().date()):
            fa.start = start
        if len(end) > 0 and end > str(datetime.today().date()) and end > str(fa.start):
            fa.end = end
        if reason != fa.reason:
            fa.reason = reason

    fa.save()
    return JsonResponse({'id': fa.id, 'message': 'Updated'})


@login_required(login_url=reverse_lazy('login'))
def delete_facility_application(request):
    FacilityApplication.objects.get(id=request.GET.get('id')).delete()

    return JsonResponse({'is_success': True})


# Remove a facility from 'items' field of an
# application list whose status is PENDING
@login_required(login_url=reverse_lazy('login'))
def remove_facility_from_list(request):
    f = Facility.objects.get(id=request.GET.get('facility_id'))
    fa = FacilityApplication.objects.get(id=request.GET.get('facility_app_id'))

    if f and fa:
        if fa.status == 'PEN' and (f in fa.items.all()):
            fa.items.remove(f)
            fa.save()
            return JsonResponse({'is_success': True})

    return JsonResponse({'is_success': False})
