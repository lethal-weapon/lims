from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy

from .forms import FacilityApplicationForm
from .models import FacilityApplication, ResearchApplication


@login_required(login_url=reverse_lazy('login'))
def my_list(request):
    return render(request, 'applications/my-list.html', {
        'facility_application_list':
            FacilityApplication.objects.filter(applicant=request.user),
        'research_application_list':
            ResearchApplication.objects.filter(applicant=request.user),
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
                'apply_message': 'Application Saved',
                'is_success'   : True,
            })

        return render(request, 'applications/apply-facility.html', {
            'apply_message': 'Please Fill Fields with Correct Input',
            'is_success'   : False,
        })


@login_required(login_url=reverse_lazy('login'))
def apply_research(request):
    return render(request, 'applications/apply-research.html', {
    })
