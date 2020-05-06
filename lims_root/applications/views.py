from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy

from accounts.models import Account
from inventory.models import Apparatus, Facility, Laboratory
from inventory.views import get_occupied_facilities
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
        'user_quota'               : get_user_quota(request.user),
    })


@login_required(login_url=reverse_lazy('login'))
def create_fa(request, template_name='applications/apply-facility.html'):
    if request.method == 'GET':
        return render(request, template_name)

    elif request.method == 'POST':
        form = FacilityApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            try:
                app.applicant = request.user
            except Exception:
                pass
            app.save()
            return render(request, template_name, {
                'apply_message': 'Application Added',
                'is_success'   : True,
            })

        return render(request, template_name, {
            'apply_message': 'Please Fill Fields with Reasonable Input',
            'is_success'   : False,
        })


@login_required(login_url=reverse_lazy('login'))
def create_ra(request, template_name='applications/apply-research.html'):
    return render(request, template_name, {
    })


@login_required(login_url=reverse_lazy('login'))
def ajax_fa_switcher(request):
    action = request.GET.get('action')

    if action == 'APPLY':
        return apply_fa(request)
    elif action == 'UPDATE':
        return update_fa(request)
    elif action == 'WITHDRAW':
        return withdraw_fa(request)
    elif action == 'DELETE':
        return delete_fa(request)


def apply_fa(request):
    replies = {
        'message'   : '',
        'is_success': False,
        'id'        : request.GET.get('id'),
    }
    fa = FacilityApplication.objects.get(id=request.GET.get('id'))
    item_count = fa.items.count()
    quota = get_user_quota(request.user)
    occupied_facilities = get_occupied_facilities()
    apparatus_ids = set([a.id for a in Apparatus.objects.all()])

    if item_count < 1:
        replies['message'] = 'Apply for WHAT exactly?'

    elif item_count > quota:
        replies['message'] = 'You can only apply additional ' + str(quota) + ' facilities!'

    elif item_count == 1:
        if fa.items.first() in occupied_facilities:
            replies['message'] = 'This facility is unavailable right now'
        else:
            replies['is_success'] = True

    else:
        # Facilities that are managed by different
        # staffs can't be applied together
        management, unavailable = {}, []
        for f in fa.items.all():
            if f in occupied_facilities:
                unavailable.append(f)

            if f.staff in management.keys():
                management[f.staff].append(f)
            else:
                management[f.staff] = [f]

        for f in unavailable:
            if f.id in apparatus_ids:
                replies['message'] += str(Apparatus.objects.get(id=f.id))
            else:
                replies['message'] += str(Laboratory.objects.get(id=f.id))
            replies['message'] += ' is unavailable! //'

        if len(management) > 1:
            for lst in management.values():
                replies['message'] += '['
                for f in lst:
                    if f.id in apparatus_ids:
                        replies['message'] += str(Apparatus.objects.get(id=f.id)) + ', '
                    else:
                        replies['message'] += str(Laboratory.objects.get(id=f.id)) + ', '
                replies['message'] += '] // '
            replies['message'] += ' need to be applied separately!'

        if len(unavailable) == 0 and len(management) == 1:
            replies['is_success'] = True

    if replies['is_success']:
        fa.applied_at = datetime.today()
        fa.status = 'APP'
        fa.save()
    return JsonResponse(replies)


def update_fa(request):
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
    return JsonResponse({'id': fa.id, 'is_success': True})


def withdraw_fa(request):
    fa = FacilityApplication.objects.get(id=request.GET.get('id'))
    fa.applied_at = None
    fa.status = 'PEN'
    fa.save()

    return JsonResponse({'is_success': True})


def delete_fa(request):
    FacilityApplication.objects.get(id=request.GET.get('id')).delete()

    return JsonResponse({'is_success': True})


def get_user_quota(user):
    fal = FacilityApplication.objects.filter(applicant=user).filter(
        status__in=['APP', 'WAI', 'BOR', 'OVE'])
    borrow_limit = Account.objects.get(id=user.id).limit
    current_count = sum([fa.items.count() for fa in fal])

    return borrow_limit - current_count


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
