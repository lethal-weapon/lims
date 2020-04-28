from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from inventory.models import Apparatus, Laboratory
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
        'context': context,
    })


@login_required(login_url=reverse_lazy('login'))
def update_facility(request, pk):
    pass


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
